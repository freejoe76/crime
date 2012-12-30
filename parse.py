#!/usr/bin/python
# Run a query against the crime CSV's
import os
import csv
import operator
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime

crime_genres = ['violent', 'property', 'other']
crime_lookup_reverse = { 
    'violent': ['murder', 'robbery', 'aggrvated-assault', 'sexual-assault'],
    'property': ['arson', 'theft-from-motor-vehicle', 'auto-theft', 'burglary', 'larceny'],
    'other': ['all-other-crimes', 'drug-alcohol', 'other-crimes-against-persons', 'white-collar-crime', 'public-disorder'] }
crime_lookup = {
    'all-other-crimes': 'other',
    'murder': 'violent',
    'arson': 'property',
    'theft-from-motor-vehicle': 'property',
    'auto-theft': 'property',
    'sexual-assault': 'violent',
    'drug-alcohol': 'other',
    'larceny': 'property',
    'aggravated-assault': 'violent',
    'other-crimes-against-persons': 'other',
    'robbery': 'violent',
    'burglary': 'property',
    'white-collar-crime': 'other',
    'public-disorder': 'other'
}
keys = ['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION','OFFENSE_TYPE_ID','OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE','LAST_OCCURRENCE_DATE','REPORTED_DATE','INCIDENT_ADDRESS','GEO_X','GEO_Y','GEO_LON','GEO_LAT','DISTRICT_ID','PRECINCT_ID','NEIGHBORHOOD_ID']
neighborhoods = ['wellshire', 'bear-valley', 'hilltop', 'cbd', 'university-hills', 'overland', 'speer', 'union-station', 'washington-virginia-vale', 'marston', 'north-capitol-hill', 'city-park', 'sloan-lake', 'five-points', 'sun-valley', 'westwood', 'cole', 'windsor', 'platt-park', 'jefferson-park', 'harvey-park', 'skyland', 'sunnyside', 'southmoor-park', 'ruby-hill', 'capitol-hill', 'barnum-west', 'harvey-park-south', 'dia', 'athmar-park', 'elyria-swansea', 'lowry-field', 'goldsmith', 'stapleton', 'chaffee-park', 'berkeley', 'washington-park', 'indian-creek', 'barnum', 'montbello', 'civic-center', 'hampden-south', 'globeville', 'city-park-west', 'clayton', 'northeast-park-hill', 'country-club', 'hale', 'mar-lee', 'lincoln-park', 'gateway-green-valley-ranch', 'west-highland', 'congress-park', 'regis', 'east-colfax', 'whittier', 'belcaro', 'hampden', 'fort-logan', 'college-view-south-platte', 'montclair', 'baker', 'kennedy', 'cherry-creek', 'cheesman-park', 'west-colfax', 'south-park-hill', 'cory-merrill', 'rosedale', 'valverde', 'university-park', 'auraria', 'north-park-hill', 'highland', 'villa-park', 'university', 'virginia-village', 'washington-park-west']

def get_location_list(location_type):
    pass
    return locations

def get_location_ranking(locations, crime_type):
    pass

def convert_timestamp(ts):
    # Take a crimestamp (UHN) from the csv and turn it into a datetime object
    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
    
def get_span_crimes(location = None, time_type = 'month', quantity = 'this',  *args, **kwargs):
    # Get crimes from a particular span of time
    pass

def get_recent_crimes(location = None, time_type = 'month', quantity = 'this',  *args, **kwargs):
    crimes = []
    if quantity == 'this':
        time = datetime.now()

    for row in crime_file:
        record = dict(zip(keys, row))
        ts = convert_timestamp(record['FIRST_OCCURRENCE_DATE'])
        if time_type == 'week':
            pass
        if time_type == 'month':
            if ts.month == time.month:
                print '1'
        elif time_type == 'year':
            if ts.year == time.year:
                print '2'
        if location == None:
            crimes.append(record['OFFENSE_CATEGORY_ID'])
        elif record['NEIGHBORHOOD_ID'] == location:
            crimes.append(record)

    pass

def get_rankings(crime=None, **kwargs):
    # Take a crime type or category and return a list of neighborhoods 
    # ranked by frequency of that crime.
    # If no crime is passed, we just rank overall number of crimes
    # for that particular time period.
    # kwargs honored include location, month (should "month" be "time"? incorporate that and "year" together?)
    rankings = { 
        'neighborhood': defaultdict(int),
        'genre': defaultdict(int),
        'category': defaultdict(int),
        'type': defaultdict(int)
    }
    for row in crime_file:
        record = dict(zip(keys, row))
        if crime == None:
            # Update the neighborhood counter
            rankings['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
            rankings['type'][record['OFFENSE_TYPE_ID']] += 1
            rankings['category'][record['OFFENSE_CATEGORY_ID']] += 1
            crime_genre = crime_lookup[record['OFFENSE_CATEGORY_ID']]
            rankings['genre'][crime_genre] += 1

        else:
            if crime == record['OFFENSE_ID'] or crime == record['OFFENSE_CATEGORY_ID']:
                rankings['neighborhood'][record['NEIGHBORHOOD_ID']] += 1


    sorted_rankings = sorted(rankings['neighborhood'].iteritems(), key=operator.itemgetter(1))
    sorted_rankings = sorted(rankings['genre'].iteritems(), key=operator.itemgetter(1))
    sorted_rankings = sorted(rankings['category'].iteritems(), key=operator.itemgetter(1))
    sorted_rankings = sorted(rankings['type'].iteritems(), key=operator.itemgetter(1))
    print sorted_rankings


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

def open_csv(fn = '_input/crime-currentyear.csv'):
    # Open the crime file for parsing.
    # It defaults to the current year's file.
    fp = open(fn, 'rb')
    crime_file = csv.reader(fp, delimiter = ',')
    return crime_file

if __name__ == '__main__':
    # parse the arguments, pass 'em to the function
    parser = OptionParser()
    parser.add_option("-a", "--action", dest="action")
    parser.add_option("-l", "--location", dest="location", default="capitol-hill")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    (options, args) = parser.parse_args()
    action = options.action
    location = options.location
    verbose = options.verbose

    location = get_neighborhood(location)

    crime_file = open_csv()
    if action == 'rankings':
        get_rankings()
    if action == 'recent':
        #get_recent_crimes(location, {'time_type':'weeks', 'quantity':3})
        get_recent_crimes(location, {'time_type':'months', 'quantity':'this'})
    #get_recent_crimes()
