# Collections of different AT commands
# NOTE: by no means, this is the complete AT cmds collection.
# Vendor-specific modems are targeting Qualcomm and Samsung
# May 25, 2017
# daveti


white_list = []

black_list = [
	"AT+USBDEBUG",
	"AT+WIFIVALUE",
    "ATD+1234567890", # Call phone number: 123-456-7890
	"ATH"		  # Hangoff the call
	]

support_list = [
	"ATD"
	]


# Add whatever sub lists here
fuzz_list = [
	(black_list, "forbidden cmds from daveti"),
	(support_list, "supported cmds from modem")
	]

# Commands known to reboot
reboot_list = [
	"AT+CRST",
	"AT+FACTORST=0,0",
	"AT+FACTORST=0,0\r",
	"ATS", # Crash atd in Nexus 5
	"ATZ",
	"AT+CFUN=1,1",
	"AT+CFUN=1,1\",",
	"AT+CFUN=1,1\'",
	"AT+CFUN=4", # G3/S8+
	"AT+CFUN=6", # G3/S8+
	"AT+CFUN=0;+CFUN=6", # Reboot G3/G4
	"AT+CFUN=6,0", # Reboot G3
	"AT+CGDATA=\"PPP\"", # Crash atd in G3 and Nexus 5
	"AT+CCHC", # Crash atd in ZenPad
	"AT+CCWA", # Crash atd in ZenPad
	"AT+COLR?", # Crash atd in ZenPad
	"AT+COUNTRST", # Reset the USB connection in ZenPad
	"AT+CTMRV", # This gets G3 stuck 4ever
	"AT+CTMRV=", # G3
	"AT+CTMRV=\"", # G3
	"AT+CTMRV=NR", # G3
	"AT+COPS", # Crash atd for G3 and maybe other phones without sim card...
	"AT+CMGS", # Crash atd for nexus 5 (not on others...)
	"AT+CMGW", # Crash atd for nexus 5 (not on others...)
	"AT+CMUX", # Crash atd in ZenPad
	"AT+CNAP?", # Crash atd in ZenPad
	"AT%MODEMRESET", # G3 modem shuts down
	"AT+CPUC?", # Crash atd on G3
	"AT+CRST=FS", # Factory reset on G3
	"AT+CUAD", # Crash atd on G3
	"AT%DRM", # These cause G3's AT distributor to crash?
	"AT%PMRST", # G3 reboot
	"AT%POWEROFF", # G3 reboot
	"AT+DI_ADJ_BATTERY_CHECK_CHARGE", # Hangs G3 again
	"AT%DLOAD", # G3/G4 download mode
	"AT%MINIOS", # G3/G4 we dont want this (testing mode)
	"AT+FUS", # Download mode for S7Edge, Note2
	"AT+FUS?", # Or maybe this one, although unlikely
	"AT%FRST", # Factory reset on G3
	"AT%RESTART", # Restart G3
	"AT%RPMBMANUALPROVISIONING", # Stuck G4, and RPMB - security!!!
	"AT^RESET", # Reset S8+ and power it off, and G4
	"AT$QCMGW", # Crash atd in s7edge
	"AT+SUDDLMOD",
	"AT+SUDDLMOD=0,0",
	"AT+C2KCMGS", # Crash atd in s7edge
	"AT+CALLCONN", # Crash atd in s7edge
	"AT+CPOS", # Crash atd in zenphone mode 2
	"AT+XEONS", # Crash atd in ZenPad
	"AT+XLOG"  # Crash atd in zenphone mode 3
	]
