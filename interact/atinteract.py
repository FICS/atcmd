#!/usr/bin/env python
import serial
import os
import time
import readline
import sys

from stat import *

#from IPython import embed

DEFAULT_BAUD=115200
DEFAULT_TIMEOUT=1

def create_serial(device, baud):
    print("Creating serial device %s @ %d baud" % (device, baud))
    return serial.Serial(device, baud, timeout=DEFAULT_TIMEOUT)

def at_probe():
    print("Probing for TTY devices...")

    found = []
    for i in xrange(10):
        devname = '/dev/ttyACM%d' % i

        if not os.path.exists(devname):
            continue

        mode = os.stat(devname).st_mode

        if S_ISCHR(mode):
            found += [devname]

    return found

def send_at_command(ser, cmd):
    ser.write(cmd + "\r")

    lines = []

    while True:
        line = ser.readline()

        # timeout
        if line == "":
            break

        # clean up the output (we dont want line endings)
        line_clean = line.strip('\r\n')

        lines += [line_clean]

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

    return lines

def enter_at_prompt(device, ser):
    while True:
        cmd = raw_input('%s > ' % device)

        if cmd == "" or cmd == "\n":
            continue

        resp = send_at_command(ser, cmd)

        for line in resp:
            print line

def at_connect(dev, baud):
    ser = create_serial(dev, 115200)

    for i in range(3):
        # See if anything is listening
        resp = send_at_command(ser, 'AT')

        if len(resp) > 0 and resp[-1] == 'OK':
            return ser

        time.sleep(1)

    ser.close()

    return None

def main():
    devices = at_probe()

    if len(devices) == 0:
        print "No devices found"
        return

    chosen_ser = None

    for dev in devices:
        ser = at_connect(dev, DEFAULT_BAUD)

        if ser is not None:
            chosen_ser = ser
            break

    if not chosen_ser:
        print('Unable to find active AT device interface')
        return

    print('Using candidate AT device %s' % dev)

    while True:
        try:
            enter_at_prompt(dev, chosen_ser)
        except serial.serialutil.SerialException as e:
            chosen_ser.close()

            if 'write failed' in e.message:
                print('Failed to send AT command: write error')
                print('Trying to reconnect to any TTY until Ctrl+C...')

                chosen_ser = None

                while not chosen_ser:
                    time.sleep(1)

                    devices = at_probe()

                    for new_dev in devices:
                        try:
                            new_serial = at_connect(new_dev, DEFAULT_BAUD)

                            if new_serial is not None:
                                chosen_ser = new_serial
                                dev = new_dev
                                break
                        except serial.serialutil.SerialException:
                            pass

                # Clear out any junk
                while chosen_ser.readline() != "":
                    time.sleep(0.5)
                    pass
            else:
                raise e
        except EOFError:
            print('\nExiting on user Ctrl+D...')
            sys.exit(0)
        except KeyboardInterrupt:
            print('\nExiting on user Ctrl+C...')
            sys.exit(0)

    # system.at-proxy.mode
    #embed()


if __name__ == "__main__":
    main()
