# AT Command mass device-testing tool: atsend.py

#### Developed by researchers from the Florida Institute for Cybersecurity Research (FICS Research)
#### Check out our webpage: <https://atcommands.org/>

This Python script (atsend.py) is used for automated testing of the effect of a large number of AT commands on a physically connected phone, using _PySerial_ to interact with the phone. _PySerial_ opens and interacts with a `/dev/ttyACM%d` device node directly, setting parameters such as baud rate and bitwidth. In our own testing, we were able to communicate ith all modems using a 115200 baud, 8-bit, no parity, 1 stop bit scheme.

##### Dependency:
`at_cmds.py` should be in the same directory as atsend.py. This file contains several lists used by atsend.py. For example, commands listed in `reboot_list` have observable effects that interrupt atsend.py, such as rebooting the phone.

##### Usage:
	./atsend.py <skipnum (optional)> <AT command list file (optional)>
	
If the script is interrupted while running due to some unexpected event on the device, it is possible to resume where you left off by designating the number of commands to skip (skipnum). Additionally, an AT command list file can be provided. This file is a text file containing one AT command per line, and each of these AT commands will be sent to the phone. The command and the associated response will be recorded in the output file: **atsend.log**.
