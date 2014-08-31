#!/bin/bash
# Publish a json file suitable for a monthly report.
# $ ./monthly.bash --location capitol-hill

# Default:
LOCATIONS=capitol-hill
while [ "$1" != "" ]; do
    case $1 in
        -l | --location ) shift
            LOCATIONS=$1
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

for LOCATION in $LOCATIONS; do
    FILENAME=reports/1-year-$LOCATION.json
    SUFFIX="--action rankings --location $LOCATION --output json --file last12months"
    #./parse.py --action rankings --file last12months --crime dv --grep --output json --location capitol-hill

    VIOLENT=`./parse.py --crime violent $SUFFIX`
    DV=`./parse.py --crime dv --grep $SUFFIX`
    PROPERTY=`./parse.py --crime property $SUFFIX`
    ROBBERY=`./parse.py --crime robbery --grep $SUFFIX`
    BURGLE=`./parse.py --crime burg --grep $SUFFIX`
    BURGLE_RESIDENCE=`./parse.py --crime burglary-residence --grep $SUFFIX`
    BURGLE_BUSINESS=`./parse.py --crime burglary-business --grep $SUFFIX`
    BURGLE_FORCED=`./parse.py --crime by-force --grep $SUFFIX`
    BURGLE_UNFORCED=`./parse.py --crime no-force --grep $SUFFIX`
    THEFT_CAR=`./parse.py --crime theft-of-motor-vehicle $SUFFIX`
    THEFT_BICYCLE=`./parse.py --crime theft-bicycle $SUFFIX`
    echo '{ "items": {' >> $FILENAME
    echo '"violent": '$VIOLENT',' >> $FILENAME
    echo '"dv": '$DV',' >> $FILENAME
    echo '"property": '$PROPERTY',' >> $FILENAME
    echo '"robbery": '$ROBBERY',' >> $FILENAME
    echo '"burgle": '$BURGLE',' >> $FILENAME
    echo '"burgle_residence": '$BURGLE_RESIDENCE',' >> $FILENAME
    echo '"burgle_business": '$BURGLE_BUSINESS',' >> $FILENAME
    echo '"burgle_forced": '$BURGLE_FORCED',' >> $FILENAME
    echo '"burgle_unforced": '$BURGLE_UNFORCED',' >> $FILENAME
    echo '"theft_car": '$THEFT_CAR',' >> $FILENAME
    echo '"theft_bicycle": '$THEFT_BICYCLE >> $FILENAME
    echo '}}' >> $FILENAME

    for MONTH in 1 2 3 4 5 6; do
        FILENAME=reports/$MONTH-month-$LOCATION.json
        > $FILENAME
        SUFFIX="--action rankings --location $LOCATION --output json --file $MONTH"monthsago
        VIOLENT=`./parse.py --crime violent $SUFFIX`
        DV=`./parse.py --crime dv --grep $SUFFIX`
        PROPERTY=`./parse.py --crime property $SUFFIX`
        ROBBERY=`./parse.py --crime robbery --grep $SUFFIX`
        BURGLE=`./parse.py --crime burg --grep $SUFFIX`
        BURGLE_RESIDENCE=`./parse.py --crime burglary-residence --grep $SUFFIX`
        BURGLE_BUSINESS=`./parse.py --crime burglary-business --grep $SUFFIX`
        BURGLE_FORCED=`./parse.py --crime by-force --grep $SUFFIX`
        BURGLE_UNFORCED=`./parse.py --crime no-force --grep $SUFFIX`
        THEFT_CAR=`./parse.py --crime theft-of-motor-vehicle $SUFFIX`
        THEFT_BICYCLE=`./parse.py --crime theft-bicycle $SUFFIX`
        echo '{ "items": {' >> $FILENAME
        echo '"violent": '$VIOLENT',' >> $FILENAME
        echo '"dv": '$DV',' >> $FILENAME
        echo '"property": '$PROPERTY',' >> $FILENAME
        echo '"robbery": '$ROBBERY',' >> $FILENAME
        echo '"burgle": '$BURGLE',' >> $FILENAME
        echo '"burgle_residence": '$BURGLE_RESIDENCE',' >> $FILENAME
        echo '"burgle_business": '$BURGLE_BUSINESS',' >> $FILENAME
        echo '"burgle_forced": '$BURGLE_FORCED',' >> $FILENAME
        echo '"burgle_unforced": '$BURGLE_UNFORCED',' >> $FILENAME
        echo '"theft_car": '$THEFT_CAR',' >> $FILENAME
        echo '"theft_bicycle": '$THEFT_BICYCLE >> $FILENAME
        #echo '"": '$','
        echo '}}' >> $FILENAME
    done
done
