#!/usr/bin/python
# Run a query against the crime CSV's
import os
import csv
import operator
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime, timedelta

# The location-specific data
from dicts import *

def abstract_keys(key):
    # Take a key, return its CSV equivalent.
    # Used so we can use this for more than just Denver crime csv.
    pass

def get_location_list(location_type):
    pass
    return locations

def get_location_ranking(locations, crime_type):
    pass

def get_timespan_crimes(location = None, time_type = 'month', quantity = 'this',  *args, **kwargs):
    # Get crimes from a particular span of time
    pass

def check_date(value):
    # Check a date to see if it's valid. If not, throw error.
    return datetime.strptime(value, '%Y-%m-%d')

def check_datetime(value):
    # Check a datetime to see if it's valid. If not, throw error.
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

def get_specific_crime(crime, grep, location = None):
    # Indexes specific crime.
    # Example: Hey, among Drug & Alcohol abuses in cap hill, is meth more popular than coke?
    # $ ./parse.py --verbose --action specific --crime meth --grep True
    # $ ./parse.py --verbose --action specific --crime cocaine --grep True
    # 
    # Returns frequency for csv specified.
    # Also returns the # of days since the last crime.
    crimes = get_recent_crimes(crime, grep, location)
    count = len(crimes['crimes'])
    last_crime = None
    if count > 0:
        last_crime = crimes['crimes'][0]['FIRST_OCCURRENCE_DATE']

    return { 'count': count, 'last_crime': last_crime, 'crime': crime }

def get_recent_crimes(crime = None, grep = False, location = None, *args, **kwargs):
    # Given a crime genre / cat / type, a location or a timespan, return a list of crimes.
    # Timespan is passed as an argument (start, finish)
    # !!! the input files aren't listed in order of occurence, so we need to sort.

    diffs = None
    crimes = []
    crime_type = get_crime_type(crime)

    if not args or args[0] == []:
        timespan = None
    else:
        # timespan a tuple of dates, that defaults to everything.
        # Decided to set that here rather than in the method def for the sake of space.
        timespan = (datetime.date(datetime.strptime(args[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(args[0][1], '%Y-%m-%d')))
        if verbose:
            print "Publishing crimes from %s to %s" % ( timespan[0].month, timespan[1].month )

    if verbose:
        print "Timespan: %s, location: %s, crime: %s" % (timespan, location, crime)

    if diff == True:
        adds = 0
        removes = 0

    for row in crime_file:
        if len(row) < 5:
            continue
        record = dict(zip(keys, row))
        #print record

        # Address diffs, if we've got 'em.
        if diff == True:
            #print record['INCIDENT_ID'][0]
            if record['INCIDENT_ID'][0] == '>':
                record['diff'] = 'add'
                adds += 1
            elif record['INCIDENT_ID'][0] == '<': 
                record['diff'] = 'remove'
                removes += 1

            # Strip the "< " at the start, and the ".0" at the end
            record['INCIDENT_ID'] = record['INCIDENT_ID'][2:-2]

        # Time queries
        if timespan:
            ts = check_datetime(record['FIRST_OCCURRENCE_DATE'])
            if not timespan[0] <= datetime.date(ts) <= timespan[1]:
                continue

        # Location, then crime queries
        # This logic tree is more like four shrubs next to each other:
        # 1. No crime and no location parameters,
        # 2. Maybe crime, but yes location,
        # 3. No crime, yes location
        # 4. Yes crime, no location 
        if location == None and crime == None:
            crimes.append(record)
            continue

        if location != None:
            if record['NEIGHBORHOOD_ID'] != location:
                continue

        if crime == None:
            crimes.append(record)
            continue

        if crime != None:
            if crime_type == 'parent_category':
                if record['OFFENSE_CATEGORY_ID'] in crime_lookup_reverse[crime]:
                    crimes.append(record)
            else:
                if record[crime_type] == crime:
                    crimes.append(record)
                elif grep == True:
                    # Loop through the types of crimes 
                    # (the lowest-level crime taxonomy), 
                    # looking for a partial string match.
                    if crime in record['OFFENSE_TYPE_ID']:
                        crimes.append(record)
    diffs = None
    if diffs == True:
        diffs = { 'adds': adds, 'removes': removes }
    return { 'crimes': crimes, 'diffs': diffs }


def get_crime_type(crime):
    # Figure out what type of crime we're querying
    # parent_category doesn't correspond to a CSV field,
    # which is why it looks different. So that's obvious.
    # type OFFENSE_TYPE_ID
    # genre violent / property / other 
    # category OFFENSE_CATEGORY_ID
    crime_type = 'OFFENSE_TYPE_ID'
    if crime in crime_genres:
        crime_type = 'parent_category'
    elif crime in crime_lookup:
        crime_type = 'OFFENSE_CATEGORY_ID'

    return crime_type


def get_rankings(crime = None, location = None, *args, **kwargs):
    # Take a crime type or category and return a list of neighborhoods 
    # ranked by frequency of that crime.
    # If no crime is passed, we just rank overall number of crimes
    # (and crimes per-capita) for that particular time period.
    # Args taken should be the start of the timespan and the end.
    rankings = { 
        'neighborhood': defaultdict(int),
        'genre': defaultdict(int),
        'category': defaultdict(int),
        'type': defaultdict(int)
    }
    percapita = { 
        'neighborhood': defaultdict(int),
        'genre': defaultdict(int),
        'category': defaultdict(int),
        'type': defaultdict(int)
    }
    percapita_multiplier = 1000
    today = datetime.date(datetime.now())
    if args[0] == []:
        month = today - timedelta(90)
        timespan = (month, today)
    else:
        timespan = (datetime.date(datetime.strptime(args[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(args[0][1], '%Y-%m-%d')))

    crime_type = get_crime_type(crime)

    for row in crime_file:
        record = dict(zip(keys, row))

        # Time queries
        ts = check_datetime(record['FIRST_OCCURRENCE_DATE'])
        if not timespan[0] <= datetime.date(ts) <= timespan[1]:
            continue

        if crime == None:
            # Update the neighborhood counter
            rankings['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
            percapita['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
            rankings['type'][record['OFFENSE_TYPE_ID']] += 1
            rankings['category'][record['OFFENSE_CATEGORY_ID']] += 1
            crime_genre = crime_lookup[record['OFFENSE_CATEGORY_ID']]
            rankings['genre'][crime_genre] += 1

        else:

            if crime == crime_lookup[record['OFFENSE_CATEGORY_ID']] or crime == record['OFFENSE_CATEGORY_ID'] or crime == record['OFFENSE_TYPE_ID']:
                #print crime, crime_lookup[record['OFFENSE_CATEGORY_ID']]
                rankings['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
                percapita['neighborhood'][record['NEIGHBORHOOD_ID']] += 1

    for item in percapita['neighborhood'].items():
        #print "Item 1: %s Pop of %s: %s" % ( item[1], item[0], populations[item[0]] ), 
        percapita['neighborhood'][item[0]] = round( float(item[1])/float(populations[item[0]]) * 1000, 2)

    sorted_rankings = {
        'neighborhood': sorted(rankings['neighborhood'].iteritems(), key=operator.itemgetter(1)),
        'percapita': sorted(percapita['neighborhood'].iteritems(), key=operator.itemgetter(1)),
        'genre': sorted(rankings['genre'].iteritems(), key=operator.itemgetter(1)),
        'category': sorted(rankings['category'].iteritems(), key=operator.itemgetter(1)),
        'type': sorted(rankings['type'].iteritems(), key=operator.itemgetter(1))
    }
    return { 'crimes': sorted_rankings }

def get_median(ranking):
    # Take a ranking dict, add up the numbers, get the median.
    pass

def get_uniques(field):
    # Write a list of unique values from a field in the CSV
    values = []
    for row in crime_file:
        record = dict(zip(keys, row))
        values.append(record[field])

    print set(values)
    return set(values)

def get_neighborhood(location):
    # If location's in the list return that location name
    if location in neighborhoods:
        return location
    return None
    
def open_csv(fn = '_input/currentyear'):
    # Open the crime file for parsing.
    # It defaults to the current year's file.
    crime_file_raw = csv.reader(open('%s.csv' % fn, 'rb'), delimiter = ',')

    # Sort the csv by the reported date (the 7th field, 6 on a 0-index,
    # because that's the only one that's guaranteed to be in the record.
    # Newest items go on top. It's possible we won't hard-code
    # this forever.
    crime_file = sorted(crime_file_raw, key=operator.itemgetter(6), reverse=True)
    return crime_file


def print_crimes(crimes, limit, *args):
    # How do we want to display the crimes?
    # Right now we're publishing them to be read in terminal.
    outputs = ''

    try:
        # Lists, probably recents, with full crime record dicts
        i = 0
        if output == 'csv':
            outputs += 'category, type, date_reported, address, lat, lon\n'

        crimes_to_print = crimes['crimes'][:limit]
        if limit == 0:
            crimes_to_print = crimes['crimes']

        for crime in crimes_to_print:
            i = i + 1
            if output == 'csv':
                outputs += '%s, %s, %s, %s, %s, %s\n' % (crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'], crime['GEO_LAT'], crime['GEO_LON'])
                continue
            outputs += '''%i. %s: %s
    Occurred: %s - %s
    Reported: %s
    %s\n\n''' % (i, crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['LAST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'])
    except:
        # Dicts
        try:
            outputs += "Denver crimes, per-capita:\n"
            i = 0
            for item in crimes['crimes']['percapita']:
                i = i + 1
                outputs += "%i. %s, %s\n" % (i, item[0], item[1])

            outputs += "Denver crimes, raw:\n"
            i = 0
            for item in crimes['crimes']['neighborhood']:
                i = i + 1
                outputs += "%i. %s, %s\n" % (i, item[0], item[1])
        except:
            # Specific
            try:
                outputs = '%i %s crimes, last one at %s' % ( crimes['count'], crimes['crime'], crimes['last_crime'] )
            except:
                print "We did not have any crimes to handle"
                raise 

    return outputs


if __name__ == '__main__':
    # Parse the arguments, pass 'em to the function
    # The three main args we use to query the crime data are
    # location, crime and timespan. location and crime are
    # passed as options, and timespan (start, finish) as the 
    # first two arguments. This may not be the best way to do it.
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", default="currentyear")
    parser.add_option("-a", "--action", dest="action")
    parser.add_option("-l", "--location", dest="location", default=None)
    parser.add_option("-t", "--limit", dest="limit", default=0)
    parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-g", "--grep", dest="grep", default=False, action="store_true")
    parser.add_option("-d", "--diff", dest="diff", default=False, action="store_true")
    parser.add_option("-o", "--output", dest="output", default=None)
    parser.add_option("-y", "--yearoveryear", dest="yearoveryear", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    (options, args) = parser.parse_args()
    filename = options.filename
    action = options.action
    location = options.location
    limit = int(options.limit)
    crime = options.crime
    grep = options.grep
    diff = options.diff
    output = options.output
    yearoveryear = options.yearoveryear
    verbose = options.verbose

    location = get_neighborhood(location)

    if verbose:
        print "Options: %s\nArgs: %s" % (options, args)

    if diff == True:
        filename = 'latestdiff'

    crime_file = open_csv("_input/%s" % filename)
    crimes = None
    if action == 'rankings':
        # Example:
        # $ ./parse.py --action rankings --crime violent '2013-01-01' '2013-02-01'
        crimes = get_rankings(crime, location, args)
        if verbose:
            print crimes
        crimes['crimes']['neighborhood'].reverse()
        crimes['crimes']['percapita'].reverse()
    elif action == 'recent':
        # Example:
        # $ ./parse.py --action recent --crime violent --location capitol-hill --output csv
        # $ ./parse.py --verbose --action recent --crime drug-alcohol --location capitol-hill --diff
        # $ ./parse.py --verbose --action recent --crime drug-alcohol --location capitol-hill
        crimes = get_recent_crimes(crime, grep, location, args)
    elif action == 'specific':
        # Example:
        # $ ./parse.py --verbose --action specific --crime drug-alcohol
        # $ ./parse.py --verbose --action specific --crime meth --grep True 
        crimes = get_specific_crime(crime, grep, location)
    #print crimes
    print print_crimes(crimes, limit)
