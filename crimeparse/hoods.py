#!/usr/bin/python
# Run a query against the crime CSV's
import os
import re
import csv
import operator
from collections import defaultdict
from optparse import OptionParser


keys = ['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION','OFFENSE_TYPE_ID','OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE','LAST_OCCURRENCE_DATE','REPORTED_DATE','INCIDENT_ADDRESS','GEO_X','GEO_Y','GEO_LON','GEO_LAT','DISTRICT_ID','PRECINCT_ID','NEIGHBORHOOD_ID']
neighborhoods = ['wellshire', 'bear-valley', 'hilltop', 'cbd', 'university-hills', 'overland', 'speer', 'union-station', 'washington-virginia-vale', 'marston', 'north-capitol-hill', 'city-park', 'sloan-lake', 'five-points', 'sun-valley', 'westwood', 'cole', 'windsor', 'platt-park', 'jefferson-park', 'harvey-park', 'skyland', 'sunnyside', 'southmoor-park', 'ruby-hill', 'capitol-hill', 'barnum-west', 'harvey-park-south', 'dia', 'athmar-park', 'elyria-swansea', 'lowry-field', 'goldsmith', 'stapleton', 'chaffee-park', 'berkeley', 'washington-park', 'indian-creek', 'barnum', 'montbello', 'civic-center', 'hampden-south', 'globeville', 'city-park-west', 'clayton', 'northeast-park-hill', 'country-club', 'hale', 'mar-lee', 'lincoln-park', 'gateway-green-valley-ranch', 'west-highland', 'congress-park', 'regis', 'east-colfax', 'whittier', 'belcaro', 'hampden', 'fort-logan', 'college-view-south-platte', 'montclair', 'baker', 'kennedy', 'cherry-creek', 'cheesman-park', 'west-colfax', 'south-park-hill', 'cory-merrill', 'rosedale', 'valverde', 'university-park', 'auraria', 'north-park-hill', 'highland', 'villa-park', 'university', 'virginia-village', 'washington-park-west']

def get_uniques(field):
    # Write a list of unique values from a field
    # in the CSV
    values = []
    for row in crime_file:
        record = dict(zip(keys, row))
        values.append(record[field])

    print set(values)

def open_csv(fn = '_input/census_neighborhood_demographics_2010.csv'):
    # Open the crime file for parsing.
    # It defaults to the current year's file.
    fp = open(fn, 'rb')
    crime_file = csv.reader(fp, delimiter = ',')
    return crime_file

def slugify(value):
    # Return a lower-case no-space string.
    # Ripped from the pages of from django.template.defaultfilters
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def build_custom_dict(field, value, key, csv):
    # Take a field column and a value column and return a dict
    print field, value
    stats_list = []
    for row in csv:
        record = dict(zip(key, row))
        if int(record[field]) != record[field] and record[field] > 0:
            field = slugify(record[field])
        else:
            field = record[field]
        stats_list.append((field, record[value]))

    return dict(stats_list)

def build_dict(csv):
    # Loop through a two-column csv. The first column should be
    # the key, the second the value. Return a dict of the csv.
    stats_list = []
    for row in csv:
        field = slugify(row[0])
        stats_list.append((field, row[1]))

    return dict(stats_list)

if __name__ == '__main__':
    # parse the arguments, pass 'em to the function
    # $ python hoods.py -f _input/neighborhood_to_population.csv
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="action")
    parser.add_option("-f", "--fn", dest="fn")
    (options, args) = parser.parse_args()
    fn = options.fn

    if fn is None:
         fn = '_input/census_neighborhood_demographics_2010.csv'
    crime_file = open_csv(fn)
    key = crime_file.next()
    print build_dict(crime_file)
    #build_custom_dict(key[1], key[2], key, crime_file)
