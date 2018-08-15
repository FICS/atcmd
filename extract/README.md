# AT Command extraction tool: atextract.sh

#### Developed by researchers from the Florida Institute for Cybersecurity Research (FICS Research)
#### Check out our webpage: <https://atcommands.org/>

**IMPORTANT: Before attempting to run the script, make sure to install the dependencies and (a) change the value of** `DEPPATH` **on line 62 or (b) manually update dependency locations in lines 65-83 while setting** `USINGDEPPATH=0` **on line 63.**

The atextract.sh script will take a packaged Android firmware image, fully extract its contents, and examine each of the contained files for strings containing AT commands. Specifically, we search for strings containing any of the following:

	AT+
	AT*
	AT!
	AT@
	AT#
	AT$
	AT%
	AT^
	AT&
	
atextract.sh will write to extract.sum (`MY_TMP`) during the run, with each line listing AT command candidate (column 2) and the name of the file it was discovered in (column 1). Before exiting, the discovered AT command candidates will be written to extract.db (`MY_OUT`).

Output files (and extracted files, if keepstuff=1) will be placed in a subdirectory of the newly created `extract` subdirectory of the current directory (directory from which atextract.sh was invoked). Within the `extract` directory are directories for each vendor processed so far, which in turn contain directories for each of that vendor's images (shares the name of the image, minus file extension). If extraction of an image needs to be rerun for whatever reason, first remove the directory corresponding to that image from the previous run under `extract/<vendor>`.

The rest of this README is organized as follows:

* Usage
* Example run
* Required setup for saving extracted contents
* Dependencies
* Usage of helper tool: combine_unsparse.sh
* Miscellaneous Logs

##### Usage:
	./atextract.sh <firmware image file> <vendor> <index> <keepstuff flag> <vendor mode (optional)>
	
          firmware image file = path to the top-level packaged archive (zip, rar, 7z, kdz, etc.)
                                (may be absolute or relative path)
          vendor = the vendor who produced the firmware image (e.g., Samsung, LG)
                   currently supported = samsung, lg, lenovo, zte, huawei, motorola, asus, aosp,
                                         nextbit, alcatel, blu, vivo, xiaomi, oneplus, oppo,
                                         lineage, htc, sony
          index = to extract multiple images at the same time, temporary directories will
                  need different indices. For best results, supply an integer value > 0.
          keepstuff = 0/1
                      if 0, will remove any extracted files after processing them
                      if 1, extracted files (e.g., filesystem contents, apps) will be kept
                            (useful for later manual inspection)
          vendor mode = some vendors will have several different image packagings
                        if so, supplying 1 as this optional argument will invoke an adjusted extraction
                        currently applies to:
                            password protected Samsung (.zip) image files from firmwarefile.com
                        extend as needed

These usage instructions will also be printed in the terminal if atextract.sh is run with no arguments (or an incorrect number of arguments). All arguments besides vendor mode are required.

##### Example run:
For purposes of illustration, consider a firmware image file named firmware1.zip by vendor1 that is located in images/vendor1/firmware1.zip. Assuming the default delete-after-extract behavior is acceptable, and assuming this is not an exceptional case (vendormode=0), we can initiate extraction as follows:

	./atextract images/vendor1/firmware1.zip vendor1 0 0
	
Notice the vendormode argument need not be supplied in the invocation. If not supplied, the value will default to 0.

Output files are available in ./extract/vendor1/firmware1

To run another extraction simultaneously, supply a different index:

	./atextract images/vendor2/firmware2.zip vendor2 5 0
	
These indices are used as postfixes to the temporary directories created in `$HOME` for handling mountable images, APKs, compressed archives, ODEX files, etc. These temporary directories will be automatically rewritten by the next run with the same index. Alternatively, they may be manually removed after extraction with no negative effects. The corresponding variables are: `DIR_TMP`, `MNT_TMP`, `APK_TMP`, `ZIP_TMP`, `ODEX_TMP`, `TAR_TMP`, and `MSC_TMP`. `JAR_TMP` simply decides the filename of the intermediate jar file output during app (APK) processing.

##### Required setup for saving extracted contents:
To have extracted contents saved (by supplying 1 for the keepstuff argument), several variables should first be adjusted prior to execution. These are:

* `MY_FULL_DIR`: when the keepstuff flag is set, contents of mountable system images, compressed archives, etc. will be saved to the value of `MY_FULL_DIR`. Unlike `MY_DIR`, this should be an absolute filepath.
* `EXTUSER` and `EXTGROUP`: when the keepstuff flag is set, saved contents will have their ownership and group changed to the designated values of `EXTUSER` and `EXTGROUP`.

##### Dependencies:
Our extract script requires a number of dependencies, which we list below. Make sure to acquire or install all of these and adjust the locations to the binaries/executables prior to running our **atextract.sh** script. If all 17 tools are placed in the same directory, this may be done by simply adjusting the DEPPATH variable.
Otherwise, manually update lines 61 through 79.

1. **simg2img**: converts Android sparse image format (simg) into mountable filesystem images (img). Sparse images may be standalone files or a collection of broken-apart chunks.
	* <https://github.com/anestisb/android-simg2img.git>
2. **dex2jar**: converts .dex files to .class files (zipped as a jar). The jar output is passed to jd-cli for further processing.
	* <https://github.com/daveti/dex2jar> (forked from <https://github.com/pxb1988/dex2jar>)
2. **jd-cli**: command line Java Decompiler that processes jar files. We apply grep to the jd-cli output to match possible AT commands. 
	* <https://github.com/kwart/jd-cmd.git>
3. **baksmali**: disassembler for the dex format used by Dalvik (Android).
	* Direct download: <https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.2b4.jar>
	* Other versions may work, but we tested with v2.2b4
4. **smali**: assembler for the dex format used by Dalvik (Android). After disassembling using baksmali, we reassemble using smali and pass the result to jadx for further processing.
   * Direct download: <https://bitbucket.org/JesusFreke/smali/downloads/smali-2.2b4.jar>
   * As with baksmali, other versions may work, but we tested with v2.2b4
5. **jadx**: dex to java decompiler. After rebuilding a dex file using smali, we apply jadx and apply grep to match possible AT commands.
	* <https://github.com/skylot/jadx>
6. **unkdz** and **undz**: unkdz will unpackage LG top-level archive (.kdz), after which undz will unpackage the nested archive (.dz).
	* <https://github.com/ehem/kdztools>
	* May encounter errors with newer LG images due to a different alignment of the partitions.
	* Separate invocations of undz are needed to extract each of the system images (system, userdata, cache, cust).
8. **updata**: unpackages the proprietary UPDATE.APP archive used by Huawei.
	* <https://github.com/marcominetti/split_updata.pl.git>
9. **unsparse**: combine_unsparse.sh, which we developed ourselves, is needed to combine unsparse system image fragments into a whole image. The offsets and number of sectors per partition or parsed from an XML file included within the firmware package.
	* Included in this repository
	* Currently, rules are available for handling unsparse files from Lenovo, Huawei, and ZTE. Unsparse files from the same vendor may require different handling (to account for variations in name of XML file, unsparse files' extensions, etc.)
	* Usage and additional details in section below
10. **sdat2img**: converts sparse Android data (.dat) files into mountable filesystem (.img).
	* <https://github.com/xpirt/sdat2img.git>
11. **flashtool**: flashtool is a flashing software for Sony phones that also makes it possible to extract sony's .sin firmware format to access the contained filesystems and ELFs.
	* Direct download: <http://www.flashtool.net/downloads_linux.php>
12. **sonyelf**: another tool needed specifically for Sony images. Needed to go deeper into the ramdisk from the kernel.elf returned by flashtool.
	* <https://github.com/osm0sis/unpackelf.git>
13. **imgtool**: unpacks Android boot images, making it possible to extract things such as usb configuration files from them.
	* Direct download: <http://newandroidbook.com/tools/imgtool.html>
14. **htcruudec**: decrypts/extracts HTC firmware images in .exe or .zip files by using known keys (and user-provided ones, if known).
	* Available on XDA Developer Forums: <https://forum.xda-developers.com/devdb/project/?id=15338#downloads>
	* We used version 3.6.5 for Linux, as it was the most updated version at the time. Newer versions may be more reliable?
	* The majority of HTC images we investigated did not require additional user-provided keys to perform successful decryption.
15. **splitqsb**: splits proprietary qsb file format from Lenovo.
	* Available on XDA Developer Forums: <https://forum.xda-developers.com/showthread.php?t=2595269>
16. **leszb**: extracts szb file format from Lenovo.
	* <https://github.com/yuanguo8/szbtool.git>
17. **unyaffs**: extracts files from a YAFFS2 file system image (Sony-specific format).
	* <https://github.com/ehlers/unyaffs.git>

##### combine_unsparse.sh:

Called by the `handle_unsparse` function. We developed combine_unsparse.sh to handle unsparse system images from several vendors: lenovo, huawei, and zte. This script will convert the unsparse system images into a whole image.

	./combine_unsparse.sh <dir> <image prefix> <XML filename> <vendor>
	
		dir = the directory containing the unsparse files
		image prefix = the prefix of the image name (system, userdata, etc.)
		XML filename = name of the XML file containing the sector size and offset information
		vendor = one of {lenovo, zte, huawei, lenovo2, huawei2}

##### Miscellaneous Logs:

* `TIZ_LOG` records any Samsung images that are recognized as TizenOS, not AndroidOS. We do not provide support for Tizen and immediately abort. The name of the image is recorded in samsung/tizen.log.
* `PAC_LOG`: Huawei, Lenovo, and ZTE images may be in .pac format, which we do not provide support for. The name of the image is recorded in <vendor>/spd_pac.log
* `SBF_LOG` and `MZF_LOG`: Motorola images may be in sbf or mzf file formats, respectively. We do not provide support for these. The name of the image is recorded in motorola/sbf.log or motorola/mzf.log, respectively.
* `RAW_LOG`: Asus images may be in raw file format, which we do not support. The name of the image is recorded in asus/raw.log.
* `KDZ_LOG`: The unkdz/kdz tools we rely on for extracting LG firmware images may fail for certain images with an unexpected format. If extraction fails, the name of the image is recored in lg/kdz.log.