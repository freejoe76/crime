#!/bin/bash
# Publish a json file suitable for a year over year report.
# Example usage:
# $ ./report.bash

./parse.py --action recent --output json --crime violent > _output/recent_violent.json
./parse.py --action recent --output json --crime murder > _output/recent_murder.json
./parse.py --action recent --output json --crime dv --grep > _output/recent_dv.json
./parse.py --action recent --output json --crime sex-aslt-rape > _output/recent_rape.json

for LOCATION in capitol-hill north-capitol-hill;
do
    ./parse.py --action recent --location $LOCATION --output json --crime murder > _output/recent_murder_$LOCATION.json
    ./parse.py --action recent --location $LOCATION --output json --crime aggravated-assault > _output/recent_assault_$LOCATION.json
    ./parse.py --action recent --location $LOCATION --output json --crime robbery > _output/recent_robbery_$LOCATION.json
done

FILENAME=_output/yoy.json
echo '{' > $FILENAME
python -m reports.yoy.yoy 2014-01-01 2014-08-31 --location capitol-hill --report rankings >> $FILENAME 
# We replace all the single quotes with double, then remove the traces of our work.
sed -i .bak "s/'/\"/g" $FILENAME
rm -f $FILENAME".bak"
python deletecomma.py $FILENAME
echo '}' >> $FILENAME







# Deprecated
for LOCATION in $XXXXXXXLOCATIONS; do
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
