#!/bin/bash
# Publish a json file suitable for a monthly report.
# $ ./monthly.bash --location capitol-hill

while [ "$1" != "" ]; do
    case $1 in
        -l | --location ) shift
            LOCATION=$1
            ;;
    esac
    shift
done
THIS_YEAR=`date +'%Y'`
LAST_YEAR=`expr $THIS_YEAR - 1`
LAST_LAST_YEAR=`expr $THIS_YEAR - 2`
THIS_MONTH=`date +'%Y-%m'`
LAST_MONTH=`date +'%Y-%m' --date='month ago'`
LAST_LAST_MONTH=`date +'%Y-%m' --date='2 months ago'`

function section
{
    divider='\n=============================================================\n=============================================================\n'
    echo -e $divider$1$divider;
}
function subsection
{
    divider='\n=============================================================\n'
    echo -e $divider$1$divider;
}

for MONTH in 1; do
    FILENAME=$MONTH-month-$LOCATION
    > $FILENAME
    SUFFIX="--action rankings --location $LOCATION --file $MONTH"monthsago" --output json"
    VIOLENT=`./parse.py --crime violent $SUFFIX`
    PROPERTY=`./parse.py --crime property $SUFFIX`
    ROBBERY=`./parse.py --crime robbery --grep $SUFFIX`
    BURGLE=`./parse.py --crime burg --grep $SUFFIX`
    BURGLE_RESIDENCE=`./parse.py --crime burglary-residence --grep $SUFFIX`
    BURGLE_BUSINESS=`./parse.py --crime burglary-business --grep $SUFFIX`
    BURGLE_FORCED=`./parse.py --crime by-force --grep $SUFFIX`
    BURGLE_UNFORCED=`./parse.py --crime no-force --grep $SUFFIX`
    THEFT_CAR=`./parse.py --crime theft-of-motor-vehicle $SUFFIX`
    THEFT_BICYCLE=`./parse.py --crime theft-bicycle $SUFFIX`
    echo '{ "items": {'
    echo '"violent": '$VIOLENT','
    echo '"property": '$PROPERTY''
    echo '}}'
done
