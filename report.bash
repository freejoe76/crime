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

> crimereport
echo "The last murder in $location"
python parse.py --action specific --crime murder --grep --location $location

echo "Recent Crimes in $location"
python parse.py --limit 20 --action recent --location $location

echo "Recent Violent Crimes in $location"
python parse.py --limit 20 --crime violent --action recent --location $location

echo "Violent-crime rankings this year in $location"
python parse.py --action rankings --crime violent --location $location

echo "Violent-crime rankings this month in $location"
python parse.py --action rankings --crime violent --location $location --filename currentmonth

echo "Property-crime rankings this year in $location"
python parse.py --action rankings --crime property --location $location

echo "Property-crime rankings this month in $location"
python parse.py --action rankings --crime property --location $location --filename currentmonth

