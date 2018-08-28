# USB Switcher Utility: usbswitcher.c

Originally found on <https://github.com/ud2/advisories/tree/master/android/samsung/nocve-2016-0004>.

* _Authors_: Roberto Paleari ([@rpaleari](https://twitter.com/rpaleari)) and Aristide Fattori ([@joystick](https://twitter.com/joystick))
* _Samsung ID_: SVE-2016-5301
* _ID_: CVE-2016-4030, CVE-2016-4031, CVE-2016-4032
* _Notification date_: 11/12/2015
* _Release date_: 11/04/2016

Modified to work for LG and HTC devices.

##### Prerequisites
* A Debian based system
* A working build environment (`apt-get install build-essential`)
* Pre-1.0 libusb (`apt-get install libusb-dev`)

##### Build:
	
	gcc -o usbswitcher usbswitcher.c -lusb

##### Usage:
To switch the USB configuration of a Samsung device:

	./usbswitcher -s
	
To switch the USB configuration of an LG device:

	./usbswitcher -l

To switch the USB configuration of an HTC device:

	./usbswitcher -h

##### Extending support:

To add support for additional vendors, provide the VENDOR ID. To differentiate between multiple devices from the same vendor, comment back in the `(dev->descriptor.idProduct == PRODUCT_ID)` check and adjust the value of variables `SAMSUNG_VENDOR_ID`/`LG_VENDOR_ID`/`HTC_VENDOR_ID`.
