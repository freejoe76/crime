#!/bin/bash
# Collate multiple information into a single report
# $ ./report.bash --location capitol-hill

while [ "$1" != "" ]; do
    case $1 in
        -l | --location ) shift
            location=$1
            ;;
    esac
    shift
done
divider='\n=============================================================\n=============================================================\n'
THIS_YEAR=`date +'%Y'`
LAST_YEAR=`expr $THIS_YEAR - 1`
THIS_MONTH=`date +'%Y-%m'`
LAST_MONTH=`date +'%Y-%m' --date='month ago'`

> crimereport
echo -e $divider"The last murder in $location"$divider
python parse.py --action specific --crime murder --grep --location $location

echo -e $divider"Recent crimes in $location"$divider
python parse.py --limit 20 --action recent --location $location

echo -e $divider"Recent Violent Crimes in $location"$divider
python parse.py --limit 20 --crime violent --action recent --location $location

echo -e $divider"Violent-crime rankings this year in $location"$divider
python parse.py --action rankings --crime violent --location $location

echo -e $divider"Violent-crime rankings this month in $location"$divider
python parse.py --action rankings --crime violent --location $location --filename currentmonth

echo -e $divider"Property-crime rankings this year in $location"$divider
python parse.py --action rankings --crime property --location $location

echo -e $divider"Property-crime rankings this month in $location"$divider
python parse.py --action rankings --crime property --location $location --filename currentmonth

