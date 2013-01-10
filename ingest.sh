#!/bin/bash
# This script downloads the current edition of the City of Denver's crime files.
# If there are changes to the file since we last downloaded it, we:
#     1. Save a copy of those differences with a timestamp
#     2. Save that copy of those differences to latestdiff.csv
#     3. Update the current-year csv with the results, currentyear.csv
# ***TODO: Incorporate a means of testing this script

cd _input
DATE=`date +'%F-%k'`
THIS_MONTH=`date +'%m'`
LAST_MONTH=`expr $THIS_MONTH - 1`
LAST_LAST_MONTH=`expr $THIS_MONTH - 2`
if [[ $LAST_MONTH -lt 1 ]]; then; $LAST_MONTH = `expr $LAST_MONTH + 12`; fi
if [[ $LAST_LAST_MONTH -lt 1 ]]; then; $LAST_LAST_MONTH = `expr $LAST_LAST_MONTH + 12`; fi

THIS_YEAR=`date +'%Y'`
LAST_YEAR=`expr $THIS_YEAR - 1`
LAST_LAST_YEAR=`expr $THIS_YEAR - 2`

touch crime-current.csv
wget -O crime-new.csv http://data.denvergov.org/download/gis/crime/csv/crime.csv
diff crime-new.csv crime-current.csv > crime-newdiff.csv
DIFFCOUNT=`cat crime-newdiff.csv | wc -l`

if [[ $DIFFCOUNT -gt 0 ]]; then
	cp crime-newdiff.csv crime-latestdiff.csv
	mv crime-newdiff.csv "crime-archive-$DATE.csv"
	mv crime-current.csv crime-old.csv
	mv crime-new.csv crime-current.csv
	grep "$THIS_YEAR-" crime-current.csv > crime-currentyear.csv
	grep "$LAST_YEAR-" crime-current.csv > crime-lastyear.csv
	grep "$THIS_YEAR-$THIS_MONTH" crime-current.csv > crime-currentmonth.csv
fi
