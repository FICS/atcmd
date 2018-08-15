#!/bin/bash

# This script will convert unsparse system images into a whole image
# arg1 = directory containing unsparse files
# arg2 = prefix of image name (system, userdata, etc.)
# arg3 = the XML file that contains sector size and offsets
# arg4 = the vendor

# no good means to deal with an image that has just 1

TEMP1="unsparse_values.txt"
MSGNO="dd_missing.txt"
INDEXFIND="indexfind.txt"
PLUSMAS=$2".zer"
TRK=1
ONEDONE=0
FIELDONE=
FIELDTWO=

grep $2 $1/$3 | head -1 | awk '{ for (i=1;i<=NF;i++) { if ($i ~ "num_partition_sectors=") print(i); if ($i ~ "start_sector=") print (i)}}' > $INDEXFIND
while read -r line
do
	if [ $ONEDONE -eq 0 ]; then
		FIELDONE=$line
		ONEDONE=1
	else
		FIELDTWO=$line
	fi
done < $INDEXFIND
#grep $2 $1/$3 | head -1 | awk -v fone=$FIELDONE -v ftwo=$FIELDTWO '{ print $fone, $ftwo}'
rm $INDEXFIND
#exit

#if [ "$4" == "lenovo" ] || [ "$4" == "zte" ]; then
#	grep $2 $1/$3 | awk '{ print $6, $8 }' | tr "\"" "\n" | grep -E '[0-9]' \
#	| paste -sd ' \n' | awk '1;1' | sed '1d' | head -n -1 | paste -sd ' \n' > $TEMP1
#elif [ "$4" == "lenovo2" ]; then
#	grep $2 $1/$3 | awk '{ print $6, $11 }' | tr "\"" "\n" | grep -E '[0-9]' \
#	| paste -sd ' \n' | awk '1;1' | sed '1d' | head -n -1 | paste -sd ' \n' > $TEMP1
#elif [ "$4" == "huawei" ]; then
#	grep $2 $1/$3 | awk '{ print $6, $13 }' | tr "\"" "\n" | grep -E '[0-9]' \
#	| paste -sd ' \n' | awk '1;1' | sed '1d' | head -n -1 | paste -sd ' \n' > $TEMP1
#elif [ "$4" == "huawei2" ]; then
#	grep $2 $1/$3 | awk '{ print $6, $8 }' | tr "\"" "\n" | grep -E '[0-9]' \
#	| paste -sd ' \n' | awk '1;1' | sed '1d' | head -n -1 | paste -sd ' \n' > $TEMP1
#fi

grep $2 $1/$3 | awk -v fone=$FIELDONE -v ftwo=$FIELDTWO '{ print $fone, $ftwo }' \
| tr "\"" "\n" | grep -E '[0-9]' | paste -sd ' \n' | awk '1;1' | sed '1d' | head -n -1 \
| paste -sd ' \n' > $TEMP1

EXTRAZS=`head -1 $TEMP1 | awk '{ print $1 }'`

echo -n > $MSGNO

awk '{print ($4 - $2 - $1)}' $TEMP1 >> $MSGNO

if [ "$4" == "lenovo" ] || [ "$4" == "huawei2" ] || [ "$4" == "zte" ]; then
	while read -r line
	do
		dd if=/dev/zero of=$1/$2"_"$TRK"x.img" bs=512 count=$line
		let TRK=TRK+1
	done < "$MSGNO"
elif [ "$4" == "huawei" ] || [ "$4" == "lenovo2" ]; then
	while read -r line
	do
		dd if=/dev/zero of=$1/$2"_"$TRK"x.unsparse" bs=512 count=$line
		let TRK=TRK+1
	done < "$MSGNO"
fi

rm $TEMP1
rm $MSGNO

cd $1

if [ "$4" == "lenovo" ] || [ "$4" == "huawei2" ] || [ "$4" == "zte" ]; then
	for i in `ls $2_*.img | sort -V`
	do
		cat $i >> $2".img"
	done
elif [ "$4" == "huawei" ] || [ "$4" == "lenovo2" ]; then
	for i in `ls $2_*.unsparse | sort -V`
	do
		cat $i >> $2".img"
	done
fi

FULLZS=`ls -l $2".img" | awk '{ print $5 }'`

# final step: add 0 (I guess to align blocks or sth?)
# the way to do this seems to be to add the same size of the first image-part

if [ "$4" == "zte" ] || [ "$2" != "system" ]; then 
# zte's system.img still follows lenovo
# seems we need to be more drastic for anything non-system (at least for Lenovo)
	dd if=/dev/zero of=$PLUSMAS bs=$FULLZS count=1
else
	dd if=/dev/zero of=$PLUSMAS bs=512 count=$EXTRAZS
fi

cat $PLUSMAS >> $2".img"
