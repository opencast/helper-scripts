#!/usr/bin/env bash

echo "generating html files"
mvn license:third-party-report > /dev/null
echo ""

for f in $(find . -name 'dependencies.html' | sort); do
	echo $f | cut -d '/' -f 3
   	python parse-licenses.py $f
	echo ""
	echo ""
done
