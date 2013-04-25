#!/usr/bin/env python
# Run a query against the crime CSV's
import os
from optparse import OptionParser
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
client = MongoClient()

from parse import Parse
# The location-specific data
import dicts


class Write:
    """ Handle writing data to MongoDB."""
    def __init__(self):
        pass


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", default="currentyear")
    parser.add_option("-a", "--action", dest="action")
    parser.add_option("-l", "--location", dest="location", default=None)
    parser.add_option("-t", "--limit", dest="limit", default=0)
    parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-g", "--grep", dest="grep", default=False, action="store_true")
    parser.add_option("-d", "--diff", dest="diff", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_option("-k", "--kill", dest="kill", default=False, action="store_true")
    (options, args) = parser.parse_args()
    filename = options.filename
    action = options.action
    location = options.location
    limit = int(options.limit)
    crime = options.crime
    grep = options.grep
    diff = options.diff
    verbose = options.verbose
    kill = options.kill

    if verbose:
        print "Options: %s\nArgs: %s" % (options, args)

    if diff == True:
        filename = 'latestdiff'

    parse = Parse("_input/%s" % filename, diff)

    location = parse.get_neighborhood(location)
    db = client['crimedenver']

    # Update the neighborhood timestamp. Yes, this will need to be modified.
    collection_name = '%s-timestamp' % location
    collection = db[collection_name]
    collection.remove()
    record = { 'timestamp': datetime.now() }
    collection.insert(record)

    # Rankings data doesn't vary by location -- it includes all locations.
    if action == 'rankings':
        collection_name = '%s-%s' % (action, crime)
    else:
        collection_name = '%s-%s' % (location, action)

    collection = db[collection_name]
    if kill == True:
        collection.remove()

    if action == 'ticker':
        # Example:
        # $ ./write.py --action ticker --location capitol-hill
        crimes = parse.get_specific_crime('murder', None, location)
        collection.insert(crimes)
        crimes = parse.get_specific_crime('rape', None, location)
        collection.insert(crimes)
        print crimes
    elif action == 'rankings':
        # Example:
        # $ ./write.py --action rankings --crime violent '2013-01-01' '2013-02-01'
        # $ ./write.py --action rankings --crime violent --kill
        crimes = parse.get_rankings(crime, location, args)
        if verbose:
            print crimes
        crimes['crimes']['neighborhood'].reverse()
        crimes['crimes']['percapita'].reverse()
        collection.insert({'neighborhood': crimes['crimes']['neighborhood']})
        collection.insert({'percapita': crimes['crimes']['percapita']})
        #print print_neighborhoods(crimes)
    elif action == 'recent':
        # Example:
        # $ ./write.py --action recent --crime violent --location capitol-hill --output csv
        # $ ./write.py --verbose --action recent --crime drug-alcohol --location capitol-hill --diff
        # $ ./write.py --verbose --action recent --crime drug-alcohol --location capitol-hill
        crimes = parse.get_recent_crimes(crime, grep, location, args)
        collection.insert(crimes['crimes'])
    elif action == 'specific':
        # Example:
        # $ ./write.py --verbose --action specific --crime drug-alcohol
        # $ ./write.py --verbose --action specific --crime meth --grep True 
        # Should return something like
        # {'count': 382, 'last_crime': '3 days ago', 'crime': None}
        crimes = parse.get_specific_crime(crime, grep, location)
        collection.insert(crimes)
