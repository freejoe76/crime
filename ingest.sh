#!/bin/bash
# This script downloads the current edition of the City of Denver's crime files.
# If there are changes to the file since we last downloaded it, we:
#     1. Save a copy of those differences with a timestamp
#     2. Save that copy of those differences to latestdiff.csv
#     3. Update the current-year csv with the results, currentyear.csv
#
# It takes two arguments:
#     -t / --test, which skips all file-writing operations except initial download
#     -n / --nodl, which skips the csv download, and assumes an existing new.csv file is in place.

TEST=0
NODOWNLOAD=0
while [ "$1" != "" ]; do
	case $1 in
		-n | --nodl ) 
			NODOWNLOAD=1
			;;
		-t | --test ) 
			TEST=1
			;;
	esac
	shift
done

if [[ $TEST -eq 1 ]]; then
	echo "TEST: $TEST"
	echo "NO DOWNLOAD? $NODOWNLOAD"
fi

cd _input
DATE=`date +'%F-%H'`
LOGFILE='logs/ingest'
touch $LOGFILE

THIS_YEAR=`date +'%Y'`
LAST_YEAR=`expr $THIS_YEAR - 1`
LAST_LAST_YEAR=`expr $THIS_YEAR - 2`

THIS_MONTH=`date +'%m'`
THIS_MONTH_FULL=`date +'%Y-%m'`
LAST_MONTH=`expr $THIS_MONTH - 1`
LAST_MONTH_FULL=$THIS_YEAR-`expr $THIS_MONTH - 1`
if [[ $LAST_MONTH -lt 1 ]]; then $LAST_MONTH=`expr $LAST_MONTH + 12`; fi

touch current.csv

# If we're testing, it's possible we won't want to download the csv.
if [[ $NODOWNLOAD -eq 0 ]]; then wget -O new.csv http://data.denvergov.org/download/gis/crime/csv/crime.csv; fi

diff new.csv current.csv > newdiff.csv
DIFFCOUNT=`cat newdiff.csv | wc -l`

if [[ $TEST -eq 1 ]]; then
	echo "# Number of diffs between new.csv and current.csv: $DIFFCOUNT"
	echo "# TEST: These are the commands that would be run."
	echo 'cp newdiff.csv latestdiff.csv'
	echo 'mv newdiff.csv "archive-'$DATE'.csv"'
	echo 'mv current.csv old.csv'
	echo 'mv new.csv current.csv'
	echo 'grep "'$THIS_YEAR'-" current.csv > currentyear.csv'
	echo 'grep "'$LAST_YEAR'-" current.csv > lastyear.csv'
	echo 'grep "'$THIS_MONTH'" current.csv > currentmonth.csv'

elif [[ $DIFFCOUNT -gt 0 ]]; then
	cp newdiff.csv latestdiff.csv
	mv newdiff.csv "archive-$DATE.csv"
	mv current.csv old.csv
	mv new.csv current.csv
	grep "$THIS_YEAR-" current.csv > currentyear.csv
	grep "$LAST_YEAR-" current.csv > lastyear.csv
	grep "$THIS_MONTH" current.csv > currentmonth.csv
fi

if [[ $TEST -eq 0 ]]; then echo "[$DATE] $DIFFCOUNT new entries" >> $LOGFILE; fi


