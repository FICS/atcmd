# AT Command interaction tool: atinteract.py

#### Developed by researchers from the Florida Institute for Cybersecurity Research (FICS Research)
#### Check out our webpage: <https://atcommands.org/>

##### Usage:
	./atinteract.py

To be used when the modem interface of the target device is active (e.g., some `/dev/ttyACM%d` is available). This script will probe for available interfaces, and if found, will spawn a shell. Once the shell is spawned, AT commands can be issued to the target device, and the response will be printed in the console.

The initial command sent to discover whether a modem interface is listening is simply `AT`, but another command could be substituted for this on line 83. Ten attempts will be made (this number can be adjusted on line 23).

If the connection suddenly drops, the script will automatically attempt to reconnect until a `CTRL+C` command is issued.
