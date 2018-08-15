# ATtention Spanned
A collection of scripts used to automatically extract Android firmware images and process them for AT commands.
These scripts may be modified for other tasks, such as extracting specific files or merely extracting base filesystem images.

The scripts are divided into directories based on their function. Refer to the READMEs contained in each
directory for usage instructions and more detailed information.

* **extract**: contains code for extracting AT commands from Android firmware images
* **interact**: contains code to spawn a shell for interactively sending AT commands to phones and observing the returned responses
* **send**: contains code for automated testing of a large number of AT commands on a physical phone, with all responses recorded in a log file
* **usbswitch**: contains code for switching a device to an alternate USB configuration and enabling the modem interface

For questions contact the first, second, or third author via email.

If you base any academic work off of ATCMD, please cite our paper:
```
@inproceedings {tian18,
  author = {Dave (Jing) Tian and Grant Hernandez and Joseph I. Choi and Vanessa Frost and Christie Ruales and Patrick Traynor and Hayawardh Vijayakumar and Lee Harrison and Amir Rahmati and Michael Grace and Kevin R. B. Butler},
  title = {ATtention Spanned: Comprehensive Vulnerability Analysis of {AT} Commands within the Android Ecosystem},
  booktitle = {27th {USENIX} Security Symposium ({USENIX} Security 18)},
  year = {2018},
  address = {Baltimore, MD},
  url = {https://www.usenix.org/conference/usenixsecurity18/presentation/tian},
  publisher = {{USENIX} Association},
}
```
