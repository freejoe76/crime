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

> crimereport
section "Trends in $location"
subsection "This month"
python parse.py --action rankings --crime violent --location $location --filename 0monthsago
subsection "Last month"
python parse.py --action rankings --crime violent --location $location --filename 1monthsago
subsection "The month prior"
python parse.py --action rankings --crime violent --location $location --filename 2monthsago

exit

section "The last murder in $location"
python parse.py --action specific --crime murder --grep --location $location

section "Recent crimes in $location"
python parse.py --limit 20 --action recent --location $location

section "Recent Violent Crimes in $location"
python parse.py --limit 20 --crime violent --action recent --location $location

section "Violent-crime rankings this year in $location"
python parse.py --action rankings --crime violent --location $location

section "Violent-crime rankings this month in $location"
python parse.py --action rankings --crime violent --location $location --filename currentmonth

section "Property-crime rankings this year in $location"
python parse.py --action rankings --crime property --location $location

section "Property-crime rankings this month in $location"
python parse.py --action rankings --crime property --location $location --filename currentmonth

