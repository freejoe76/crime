#!/bin/bash
# NOTE: Using this on a Mac? The Mac's default date command is insufficient.
# Download a better version using the instructions here:
# http://www.topbug.net/blog/2013/04/14/install-and-use-gnu-command-line-tools-in-mac-os-x/
#
#
# This script downloads the City of Denver's reported crime CSV.
# If there are changes to the file since we last downloaded it, we:
#     1. Save a copy of those differences with a timestamp
#     2. Save that copy of those differences to latest.diff
#     3. Update the current-year csv with the results, currentyear.csv
#
# It accepts three arguments:
#     -t / --test, which skips all file-writing operations except initial download
#     -n / --nodl, which skips the initial download, and assumes an existing new.csv file is in place.
#     -l / --location, for building archives on a particular location.
### * Note: Should look at the diffs and see at what age the data stops changing. From there,
### can build a more refined archiving (and then, querying) strategy.

source local.bash

TEST=0
NODOWNLOAD=0
URL='http://data.denvergov.org/download/gis/crime/csv/crime.csv'
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
		-u | --url ) 
			URL=$1
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
        wget -O new-unsorted.csv $URL; 
        FILESIZE=$(du -b "new-unsorted.csv" | cut -f 1)
    done
fi


# 1. Sort the downloaded CSV, new-unsorted.
# 2. Run a diff between new-unsorted and the current (previous day's) csv, current.csv
# 3. If there are differences btw the CSVs, run the rest of this script.
cat head.csv > new.csv; tail -n +2 new-unsorted.csv | sort -r >> new.csv 
diff new.csv current.csv > new.diff
DIFFCOUNT=`cat new.diff | wc -l`

if [[ $TEST -eq 1 ]]; then
	echo "# Number of diffs between new.csv and current.csv: $DIFFCOUNT"
	echo "# TEST: These are the commands that would be run."
	echo 'cp new.diff latest.diff'
	echo 'mv new.diff "archive-'$DATE'.diff"'
    echo './processdiff.py new.diff > "archive-$DATE.csv"'
	echo 'mv current.csv old.csv'
	echo 'mv new.csv current.csv'
	echo './matchline.py "'$THIS_YEAR'-" current.csv > currentyear.csv'
	echo './matchline.py "'$LAST_YEAR'-" current.csv > lastyear.csv'
	echo './matchline.py "'$THIS_MONTH'" current.csv > currentmonth.csv'

elif [[ $DIFFCOUNT -gt 0 ]]; then
	cp new.diff latest.diff
	cp new.diff "archive-$DATE.diff"
    ./processdiff.py new.diff > "archive-$DATE.csv"
	mv current.csv old.csv
	#sort new.csv -r > current.csv
    mv new.csv current.csv
    rm new-unsorted.csv
    echo $DATE > ../latest
else
    echo "NO NEW CRIMES."
fi

# We run these operations if there are differences, or if we've set NODOWNLOAD.
if [[ $DIFFCOUNT -gt 0 || $NODOWNLOAD -eq 1 ]]; then
	./matchline.py "$THIS_YEAR-" current.csv > currentyear.csv &
	./matchline.py "$THIS_YEAR-" current.csv > $THIS_YEAR.csv &
	./matchline.py "$LAST_YEAR-" current.csv > lastyear.csv &
	./matchline.py "$THIS_YEAR-$THIS_MONTH" current.csv > currentmonth.csv &

    # Build a csv of the crimes for the last 0-12 months
    for MONTHNUM in {0..12}; do > $MONTHNUM"monthsago.csv"; done
    for MONTHNUM in {0..12}; do > "last"$MONTHNUM"months.csv"; done
    for NUM in {0..11}; do
        # We only grep into a month's file if the X in lastXmonths (X being MONTHNUM)
        # is less than or equal to the NUM+1 we're looping through.
        # So, if we're on MONTHNUM 12, NUMs 0-11 will be fine. 
        # If we're on MONTHNUM 1, only NUM 0 will be grepped.
        #
        # Ex:
        # January 2014.
        # First NUM loop: NUM = 0, TEMPNUM = 1, MONTHNUM { 0 } months ago = 0, grep 2014-01 current.csv >> last0months
        # Second NUM loop: NUM = 1, TEMPNUM = 2, MONTHNUM { 0 1 } months ago = 0 1, grep 2014-01 + 2013-12 current.csv >> last0 + 1monthsago
        # Third NUM loop: NUM = 2, TEMPNUM = 3, MONTHNUM { 0 1 2 } months ago = 0 1, grep 2014-01 + 2013-12 current.csv >> last0 + 1monthsago
        echo '======'$NUM'======'
        for MONTHNUM in {1..12}; do
            TEMPNUM=$(($NUM + 1))
            if [ $MONTHNUM -gt $TEMPNUM ]; then
                echo $MONTHNUM
                ./matchline.py `date +'%Y-%m' --date="$NUM months ago"` current.csv >> "last"$MONTHNUM"months.csv"
            fi
        done
        echo '======'
        ./matchline.py `date +'%Y-%m' --date="$NUM months ago"` current.csv >> $NUM"monthsago.csv"
    done

    # Build a csv of the crimes for the last 24, 48, 60, 72 months
    for MONTH in 24 36 48 60; do
        > last$MONTH"months.csv"
        > last$MONTH"months.txt"
    done

    #for NUM in {0..23}; do
    for NUM in {0..59}; do
        YEARMONTH=`date +'%Y-%m' --date="$NUM months ago"`
        for MONTH in 24 36 48 60; do
            if [[ $NUM -lt $MONTH ]]; then
                ./matchline.py $YEARMONTH current.csv >> last$MONTH"months.csv"
                echo $YEARMONTH >> last$MONTH"months.txt"
            fi
        done

        # We don't need month-by-month neighborhood CSVs for more than the two previous years.
        #if [[ $NUM -gt 23 ]]; then continue; fi

        echo $NUM 
        date
    done

    for NUM in {0..23}; do
        YEARMONTH=`date +'%Y-%m' --date="$NUM months ago"`
        for HOOD in ${HOODS[@]}; do
            # We include the comma in the grep to distinguish btw, say,
            # north-capitol-hill and capitol-hill. It's a CSV, the comma's the delimiter.
            ./matchline.py $YEARMONTH current.csv | grep ,$HOOD > location_$HOOD-$YEARMONTH.csv
        done
    done

    for HOOD in ${HOODS[@]}; do
        ./matchline.py $THIS_YEAR current.csv | grep ,$HOOD >> location_$HOOD-$THIS_YEAR.csv &
        ./matchline.py $LAST_YEAR current.csv | grep ,$HOOD >> location_$HOOD-$LAST_YEAR.csv
        ./matchline.py $LAST_LAST_YEAR current.csv | grep ,$HOOD >> location_$HOOD-$LAST_LAST_YEAR.csv

        # Look for what's changed since the last time.
        # This saves all the changes that happened in a month in a monnth file,
        # and the most recent set of changes.
        grep ,$HOOD archive-$DATE.csv >> location_$HOOD_archive-`date +'%Y-%m'`.csv
        grep ,$HOOD archive-$DATE.csv > location_$HOOD_archive.csv
    done

    for CRIME in ${CRIMES[@]}; do
        # Look for what's changed since the last time.
        # This saves all the changes that happened in a month in a monnth file,
        # and the most recent set of changes.
        grep ,$HOOD archive-$DATE.csv >> location_$HOOD_archive-`date +'%Y-%m'`.csv
        grep ,$HOOD archive-$DATE.csv > location_$HOOD_archive.csv
    done

    # Just because we might need it: A text file of the last yearmonth pairs for the last ten years.
    > last.txt
    for NUM in {0..120}
    do
        date +'%Y-%m' --date="$NUM months ago" >> last.txt
    done
fi

if [[ $TEST -eq 0 ]]; then echo "[$DATE] $DIFFCOUNT new entries" >> $LOGFILE; fi
date
