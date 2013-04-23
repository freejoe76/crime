#!/bin/bash
# Get the new crime csv, if there is one, and if there is, then
# update the database.
# $ ./update.bash

while [ "$1" != "" ]; do
    case $1 in
        -l | --location ) shift
            location=$1
            ;;
    esac
    shift
done
divider='\n=============================================================\n=============================================================\n'

python parse.py --action specific --crime murder --grep --location $location

python parse.py --limit 20 --action recent --location $location

python parse.py --limit 20 --crime violent --action recent --location $location

python parse.py --action rankings --crime violent --location $location

python parse.py --action rankings --crime violent --location $location --filename currentmonth

python parse.py --action rankings --crime property --location $location

python parse.py --action rankings --crime property --location $location --filename currentmonth

