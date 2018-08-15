#!/usr/bin/python

# atsend.py
# AT sender (based on mfuzz)
# Jul 6, 2017
#
# Modem Fuzzer
# Fuzzing the CDC/ACM interface exposed by cellphones
# Dep: pyserial
# May 26, 2017
#
# Added supported for reading more at cmds from a file
# Jun 13, 2017
#
# daveti

import sys
import time
import logging
import serial
import at_cmds


# Global vars
log_file = "atsend.log"
log_level = logging.DEBUG
acm_device = "/dev/ttyACM0"
baud_rate = 115200
time_out = 1
mfuzz_port = None
max_poll = 4
poll_delay = 2
format_string = ["<value>", "%d", "%u", "%s", "%c", "%x", "<n>", "<index>", "<args>", "<gain>"]
debug_cmd_gen = True



def generate(cmd, pattern, idx):
	# NOTE: hardcode values here but should be random in fuzzing mode
	# TODO: format string with width, e.g., %02d
	gen = ""
	if pattern == "<value>":
		gen = "1"
	elif pattern == "%d":
		gen = "2"
	elif pattern == "%u":
		gen = "3"
	elif pattern == "%s":
		gen = "daveti"
	elif pattern == "%c":
		gen = "a"
	elif pattern == "%x":
		gen = "f"
	elif pattern == "<n>":
		gen = "4"
	elif pattern == "<index>":
		gen = "5"
	elif pattern == "<args>":
		gen = "6"
	elif pattern == "<gain>":
		gen = "7"
	else:
		gen = "error"
		print("Error: unsupported pattern %s" % pattern)

	if gen == "error":
		return cmd

	return cmd[:idx]+gen+cmd[idx+len(pattern):]


def make(cmd):
	'''
	Generate a concrete AT cmd if the given cmd is a template
	'''
	cmd2 = "stop"
	for p in format_string:
		idx = cmd.find(p)
		if idx != -1:
			cmd2 = generate(cmd, p, idx)
			cmd = cmd2
	# Hardcode the value but should be random in fuzzing mode
	if cmd.endswith("="):
		cmd += "abc"

	if cmd2 == "stop":
		return cmd

	return make(cmd)


def recv():
	my_poll = 0
	lines = []

	# Make sure we dont go _too_ fast
	start_time = time.time()

	# To deal with the response delay
	while my_poll < max_poll:
		line = mfuzz_port.readline()

		# timeout
		if line == "":
			my_poll += 1
			time.sleep(poll_delay)
			continue

		# clean up the output for comparison
		line_clean = line.strip('\r\n')
	
		lines += [line]
	
		# a terminal response. end NOW
		if 'ERROR' == line_clean:
			break
		elif 'CME ERROR' in line_clean:
			break
		elif 'OK' == line_clean:
			break
		elif 'NO CARRIER' == line_clean:
			break
		elif 'ABORTED' == line_clean:
			break
		elif 'NOT SUPPORTED' == line_clean:
			break
		else:
			continue

	# "Do you know how fast you were going?"
	if time.time() - start_time < 1.0:
		time.sleep(1)
	
	# post-processing
	lines2 = []
	for l in lines:
		if l == '\r\n':
			continue
		if l.endswith('\r\n'):
			lines2.append(l[:-1])
	return lines2


def send(cmd):
	'''
	True - sending failed
	False - sending successful
	'''
	cmd2 = make(cmd)
	if debug_cmd_gen:
		logging.info("[%s] -> [%s]" % (cmd, cmd2))
	return (mfuzz_port.write(cmd2+'\r') != (len(cmd2)+1))


def extend(cmds):
	'''
	Extend the cmd list
	'''
	cmds2 = []
	for c in cmds:
		cmds2.append(c)
		if c.endswith("="):
			cmds2.append(c[:-1])
	return cmds2
	

def fuzz(skip_reboot, skip_num=-1, from_file=""):
	global mfuzz_port
	# Open the serial port
	mfuzz_port = serial.Serial(acm_device, baud_rate, timeout=time_out)
	if not mfuzz_port.isOpen():
		logging.error("unable to open the port %s" % acm_device)
		return
	logging.info("port is opened for %s" % acm_device)
	logging.info("skip_num: %d, from_file %s" % (skip_num, from_file))

	# Fuzz
	counter = 0
	if from_file != "":
		logging.info("fuzzing: loading at cmds from %s" % from_file)
		logging.info("----------------------------------")
		at_file = open(from_file, "r")
		at_lines = at_file.readlines()
		at_lines = [l.strip() for l in at_lines]
		at_lines = extend(at_lines)
		for c in at_lines:
			if c.startswith("#"):
				continue
			counter += 1
			if skip_num != -1 and counter <= skip_num:
				logging.info("idx [%d], cmd [%s], skipped" % (counter, c))
				continue

			skip = False
			if skip_reboot:
				for _cmd in at_cmds.reboot_list:
					if c.startswith(_cmd):
						skip = True
						break
			if skip:
				logging.info("idx [%d], cmd [%s], skipped due to reboot/reset" % (counter, c))
				continue
			if send(c):
				logging.error("idx [%d], cmd [%s], sending failed" % (counter, c))
				continue
			r = recv()
			logging.info("idx [%d], cmd [%s], response [%s]" % (counter, c, r))

		# Close the port
		mfuzz_port.close()
		logging.info("port is closed")
		sys.exit(0)

	for (sub, des) in at_cmds.fuzz_list:
		logging.info("fuzzing: %s" % des)
		logging.info("----------------------------------")
		for c in sub:
			counter += 1
			if skip_num != -1 and counter <= skip_num:
				logging.info("idx [%d], cmd [%s], skipped" % (counter, c))
				continue

			skip = False
			if skip_reboot:
				for _cmd in at_cmds.reboot_list:
					if c.startswith(_cmd):
						skip = True
						break
			if skip:
				logging.info("idx [%d], cmd [%s], skipped due to reboot/reset" % (counter, c))
				continue
			if send(c):
				logging.error("idx [%d], cmd [%s], sending failed" % (counter, c))
				continue
			r = recv()
			logging.info("idx [%d], cmd [%s], response [%s]" % (counter, c, r))

	# Close the port
	mfuzz_port.close()
	logging.info("port is closed")


def main(argv):
	# Set up the log
	logging.basicConfig(filename=log_file, level=log_level)
	logging.info("atsend/mfuzz starts...")
	# Only care about the first argument
	if len(argv) == 0:
		fuzz(True)
	elif len(argv) == 1:
		if argv[0].isdigit():
			fuzz(True, skip_num=argv[0])
		else:
			fuzz(True, from_file=argv[0])
	elif len(argv) == 2:
		fuzz(True, skip_num=int(argv[0]), from_file=argv[1])
	else:
		print("Error: only 1 argument should be provided")
	logging.info("atsend/mfuzz ends...")


if __name__ == "__main__":
	main(sys.argv[1:])

