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
#     -l / --location, for building archives on a particular location.
### * Note: Should look at the diffs and see at what age the data stops changing. From there,
### can build a more refined archiving (and, thus, querying) strategy.

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
		-l | --location ) 
			LOCATION=$1
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
LOGFILE='../logs/ingest'
touch $LOGFILE

THIS_YEAR=`date +'%Y'`
LAST_YEAR=`expr $THIS_YEAR - 1`
LAST_LAST_YEAR=`expr $THIS_YEAR - 2`

THIS_MONTH=`date +'%Y-%m'`
LAST_MONTH=`date +'%Y-%m' --date='month ago'`

touch current.csv

# If we're testing, it's possible we won't want to download the csv.
if [[ $NODOWNLOAD -eq 0 ]]; then 
    FILESIZE=0
    while [ $FILESIZE -lt 40000 ]; do
        echo "Filesize: $FILESIZE"
        wget -O new.csv http://data.denvergov.org/download/gis/crime/csv/crime.csv; 
        FILESIZE=$(du -b "new.csv" | cut -f 1)
    done
fi

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
    echo $DATE > ../latest

fi

# We run these operations if there are differences, or if we've set NODOWNLOAD.
if [[ $DIFFCOUNT -gt 0 || $NODOWNLOAD -eq 1 ]]; then
	grep "$THIS_YEAR-" current.csv > currentyear.csv
	grep "$LAST_YEAR-" current.csv > lastyear.csv
	grep "$THIS_MONTH" current.csv > currentmonth.csv

    # Build a csv of the crimes for the last 0-12 months
    for MONTHNUM in {1..12}; do > $MONTHNUM"monthsago.csv"; done
    for MONTHNUM in {1..12}; do > "last"$MONTHNUM"months.csv"; done
    for NUM in {0..11}; do
        # We only grep into a month's file if the X in lastXmonths (X being MONTHNUM)
        # is less than or equal to the NUM+1 we're looping through.
        # So, if we're on MONTHNUM 12, NUMs 0-11 will be fine. 
        # If we're on MONTHNUM 1, only NUM 0 will be grepped.
        # Ex:
        # January 2014.
        # First NUM loop: NUM = 0, TEMPNUM = 1, MONTHNUM { 0 } months ago = 0, grep 2014-01 current.csv >> 0monthsago
        # Second NUM loop: NUM = 1, TEMPNUM = 2, MONTHNUM { 0 1 } months ago = 0 1, grep 2014-01 current.csv >> 0monthsago
        # WAIT *** MONTHNUM should loop btw 0..11 and NUM btw 1..12 and we don't need TEMPNUM
        for MONTHNUM in {1..12}; do
            TEMPNUM=$(($NUM + 1))
            if [ $MONTHNUM -le $TEMPNUM ]; then
                grep `date +'%Y-%m' --date="$NUM months ago"` current.csv >> "last"$MONTHNUM"months.csv"
            fi
        done
        grep `date +'%Y-%m' --date="$NUM months ago"` current.csv >> $NUM"monthsago.csv"
    done

    # Build a csv of the crimes for the last 24 months
    > last24months.csv
    > last24months.txt
    for NUM in {0..23}; 
    do
        YEARMONTH=`date +'%Y-%m' --date="$NUM months ago"`
        grep $YEARMONTH current.csv >> last24months.csv
        for HOOD in capitol-hill civic-center;
        do
            grep $YEARMONTH current.csv | grep $HOOD >> location_$HOOD-$YEARMONTH.csv
        done
        echo $YEARMONTH >> last24months.txt
    done
    for HOOD in capitol-hill civic-center;
    do
        grep $THIS_YEAR current.csv | grep $HOOD >> location_$HOOD-$THIS_YEAR.csv
        grep $LAST_YEAR current.csv | grep $HOOD >> location_$HOOD-$LAST_YEAR.csv
        grep $LAST_LAST_YEAR current.csv | grep $HOOD >> location_$HOOD-$LAST_LAST_YEAR.csv
    done

    # Just because we might need it: A text file of the last yearmonth pairs for the last ten years.
    > last.txt
    for NUM in {0..120}
    do
        date +'%Y-%m' --date="$NUM months ago" >> last.txt
    done
fi

if [[ $TEST -eq 0 ]]; then echo "[$DATE] $DIFFCOUNT new entries" >> $LOGFILE; fi
