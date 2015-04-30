#!/bin/bash

if [ "$1" ]; then
	testscript="$1"
else
	testscript="ls *.pl"
fi

if [ "$2" ]; then
	sourcedir="$2"
else
	sourcedir="."
fi

for d in "$sourcedir"/????????-*; do
	if [ -d "$d" ]; then
		(cd $d && $testscript > test.log 2>&1) && echo TRUE || echo FALSE
	fi
done