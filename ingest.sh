#!/bin/bash
# This script downloads the current edition of the City of Denver's crime files.
# If there are changes to the file since we last downloaded it, we:
#     1. Save a copy of those differences with a timestamp
#     2. Save that copy of those differences to latestdiff.csv
#     3. Update the current-year csv with the results, currentyear.csv

cd _input
DATE=`date +'%F-%k'`
touch crime-current.csv
wget -O crime-new.csv http://data.denvergov.org/download/gis/crime/csv/crime.csv
diff crime-new.csv crime-current.csv > crime-newdiff.csv
DIFFCOUNT=`cat crime-newdiff.csv | wc -l`

if [[ $DIFFCOUNT -gt 0 ]]; then
	cp crime-newdiff.csv crime-latestdiff.csv
	mv crime-newdiff.csv "crime-archive-$DATE.csv"
	mv crime-current.csv crime-old.csv
	mv crime-new.csv crime-current.csv
	grep '2013-' crime-current.csv > crime-currentyear.csv
fi
