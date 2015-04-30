#!/bin/bash

if [ -z "$1" ]; then
	echo "usage: $0 <zipfile>"
fi


function get_field() {
	grep "^$1:" "$f" | sed 's/^'"$1"': \(.*\)$'"/\1/" |tr -d "\r"
}

zipfile="$1"
tempdir="/tmp/extract-submission-$$-$USER"

ex1dir=$tempdir/ex1dir
prefix="submissions"
mkdir -p "$prefix"
logfile="$prefix/extract.log"

date > "$logfile"

infofile="$prefix/info.csv"
echo "extracted from $zipfile" > "$infofile"

rm -f "$infofile"

mkdir -p "$ex1dir"

unzip -d "$ex1dir" "$zipfile">> "$logfile" 2>&1 || echo "*** couldn't unzip $zipfile"

for f in "$ex1dir"/*.txt; do
	name=`get_field Name`
	date=`get_field "Date Submitted"`
	#name=`grep '^Name:' "$f" | sed 's/^Name:\(.*\)$/\1/'`
	files=`grep "^\tFilename:" "$f" | sed 's/^.*Filename: \(.*\)$/\1/'|tr -d "\r"`
	echo "   extracting $name"
	sid=`echo $name | sed 's/.*(\([0-9]*\)).*/\1/'`
	#echo "$sid"
	
	clean_name=`echo "$name" | tr " " "_" | sed 's/_([0-9]*)$//'`
	ex2dir="$prefix/$sid-$clean_name"
	mkdir -p "$ex2dir"

	rm -f "$ex2dir"/*
	fileformat="none"
	if echo "$files" | grep -i -q '.zip$'; then
		unzip -j -d "$ex2dir" "$ex1dir/$files" >> "$logfile" 2>&1 || echo "*** couldn't unzip $ex1dir/$files"
		fileformat="zip"
		sub_files=`ls "$ex2dir"`
	else
    	if echo "$files" | grep -i -q '.rar$'; then
			echo "RARFILE $files" > "$ex2dir"/WRONGFILEFORMAT
			(cd $ex2dir && unrar e "$ex1dir/$files")  >> "$logfile" 2>&1 || echo "*** couldn't unrar $ex1dir/$files"
			fileformat="rar"
		else
			echo "$files" > "$ex2dir"/WRONGFILEFORMAT
		fi
	fi
	sub_files=`ls "$ex2dir" | tr "\n" " " | tr "\t" " " | tr -s " "`
	cp "$f" "$ex2dir"/submission.txt
	echo "\"$sid\",\"$name\",\"$date\",\"$fileformat\",\"$files\",\"$sub_files\"" >> $infofile

	#unzip -d "$ex2dir" "$ex1dir/$files"
	#ls "$ex1dir/$files"

	#echo "Files: $files"
done


rm -rf "$tempdir"
