#!/bin/bash
# This script downloads the current edition of the City of Denver's crime files.
# If there are changes to the file since we last downloaded it, we:
#     1. Save a copy of those differences with a timestamp
#     2. Save that copy of those differences to latestdiff.csv
#     3. Update the current-year csv with the results, currentyear.csv
# ***TODO: Incorporate a means of testing this script

cd _input
DATE=`date +'%F-%k'`
LOGFILE='logs/ingest'

THIS_YEAR=`date +'%Y'`
LAST_YEAR=`expr $THIS_YEAR - 1`
LAST_LAST_YEAR=`expr $THIS_YEAR - 2`

THIS_MONTH=`date + '%m'`
THIS_MONTH_FULL=`date +'%Y-%m'`
LAST_MONTH=`expr $THIS_MONTH - 1`
LAST_MONTH_FULL=$THIS_YEAR-`expr $THIS_MONTH - 1`
if [[ $LAST_MONTH -lt 1 ]]; then $LAST_MONTH = `expr $LAST_MONTH + 12`; fi

touch current.csv
wget -O new.csv http://data.denvergov.org/download/gis/crime/csv/crime.csv
diff new.csv current.csv > newdiff.csv
DIFFCOUNT=`cat newdiff.csv | wc -l`

if [[ $DIFFCOUNT -gt 0 ]]; then
	cp newdiff.csv latestdiff.csv
	mv newdiff.csv "archive-$DATE.csv"
	mv current.csv old.csv
	mv new.csv current.csv
	grep "$THIS_YEAR-" current.csv > currentyear.csv
	grep "$LAST_YEAR-" current.csv > lastyear.csv
	grep "$THIS_MONTH" current.csv > currentmonth.csv
fi

echo "[$DATE] $DIFFCOUNT new entries" >> $LOGFILE


