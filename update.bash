#!/bin/bash
# Get the new crime csv, if there is one, and if there is, then
# update the database.
# Sometimes we may not want to download the csv.
# $ ./update.bash

while [ "$1" != "" ]; do
    case $1 in
        -c | --csv ) shift
            csv=$1
            ;;
    esac
    shift
done

LOCATIONS='capitol-hill'
for location in $LOCATIONS; 
do 
  echo $location
  python write.py --kill --action ticker --crime murder --grep --location $location
  python write.py --kill --action recent --location $location
  #python write.py --kill --crime violent --action recent --location $location
  python write.py --action rankings --crime violent --location $location
  #python write.py --action rankings --crime violent --location $location --filename currentmonth
  python write.py --kill --action rankings --crime property --location $location
  #python write.py --kill --action rankings --crime property --location $location --filename currentmonth
done
