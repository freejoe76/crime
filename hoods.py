#!/usr/bin/python
# Run a query against the crime CSV's
import os
import csv
import operator
from collections import defaultdict
from optparse import OptionParser


keys = ['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION','OFFENSE_TYPE_ID','OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE','LAST_OCCURRENCE_DATE','REPORTED_DATE','INCIDENT_ADDRESS','GEO_X','GEO_Y','GEO_LON','GEO_LAT','DISTRICT_ID','PRECINCT_ID','NEIGHBORHOOD_ID']
neighborhoods = ['wellshire', 'bear-valley', 'hilltop', 'cbd', 'university-hills', 'overland', 'speer', 'union-station', 'washington-virginia-vale', 'marston', 'north-capitol-hill', 'city-park', 'sloan-lake', 'five-points', 'sun-valley', 'westwood', 'cole', 'windsor', 'platt-park', 'jefferson-park', 'harvey-park', 'skyland', 'sunnyside', 'southmoor-park', 'ruby-hill', 'capitol-hill', 'barnum-west', 'harvey-park-south', 'dia', 'athmar-park', 'elyria-swansea', 'lowry-field', 'goldsmith', 'stapleton', 'chaffee-park', 'berkeley', 'washington-park', 'indian-creek', 'barnum', 'montbello', 'civic-center', 'hampden-south', 'globeville', 'city-park-west', 'clayton', 'northeast-park-hill', 'country-club', 'hale', 'mar-lee', 'lincoln-park', 'gateway-green-valley-ranch', 'west-highland', 'congress-park', 'regis', 'east-colfax', 'whittier', 'belcaro', 'hampden', 'fort-logan', 'college-view-south-platte', 'montclair', 'baker', 'kennedy', 'cherry-creek', 'cheesman-park', 'west-colfax', 'south-park-hill', 'cory-merrill', 'rosedale', 'valverde', 'university-park', 'auraria', 'north-park-hill', 'highland', 'villa-park', 'university', 'virginia-village', 'washington-park-west']

def top_row(row):
    # Take the top row of a CSV and turn that into a list we can use.
    print row

def get_uniques(field):
    # Write a list of unique values from a field
    # in the CSV
    values = []
    for row in crime_file:
        record = dict(zip(keys, row))
        values.append(record[field])

    print set(values)

def get_neighborhood(location):
    # If location's in the list return that location name,
    # if not, return false
    if location in neighborhoods:
        return location

    return False

def open_csv(fn = '_input/census_neighborhood_demographics_2010.csv'):
    # Open the crime file for parsing.
    # It defaults to the current year's file.
    fp = open(fn, 'rb')
    crime_file = csv.reader(fp, delimiter = ',')
    return crime_file

if __name__ == '__main__':
    # parse the arguments, pass 'em to the function
    parser = OptionParser()
    parser.add_option("-n", "--name", dest="action")
    parser.add_option("-f", "--fn", dest="fn")
    (options, args) = parser.parse_args()
    fn = options.fn

    if fn is None:
         fn = '_input/census_neighborhood_demographics_2010.csv'
    crime_file = open_csv(fn)
    key = crime_file.next()
