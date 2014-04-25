#!/bin/bash

for YEAR in 2013 2012 2011 2010; do
    ./matchline.py $YEAR current.csv > $YEAR.csv
done
