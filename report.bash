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
echo "Recent Crimes in $location"
python parse.py --limit 20 --action recent --location $1
