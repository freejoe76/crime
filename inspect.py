#!/usr/bin/env python
# See what data we have stored for an object.
# Currently only supports neighborhoods.
import os
from optparse import OptionParser
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
client = MongoClient()

from parse import Parse
# The location-specific data
import dicts


class Inspect:
    """ Inspect data in the database."""
    def __init__(self):
        pass


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-a", "--action", dest="action", default=None)
    parser.add_option("-l", "--location", dest="location", default=None)
    parser.add_option("-t", "--limit", dest="limit", default=0)
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    (options, args) = parser.parse_args()
    action = options.action
    location = options.location
    limit = int(options.limit)
    #crime = options.crime
    verbose = options.verbose

    if verbose:
        print "Options: %s\nArgs: %s" % (options, args)

    #location = parse.get_neighborhood(location)
    db = client['crimedenver']

    
    actions = ['ticker', 'rankings', 'recent', 'specific']
    if action:
        actions = [action]

    for action in actions:
        if action == 'ticker':
            collection_name = '%s-%s' % (location, action)
            collection = db[collection_name]
            print collection.find()
        elif action == 'rankings':
            collection_name = '%s-%s' % (location, action)
            collection = db[collection_name]
            crimes = parse.get_rankings(crime, location, args)
            crimes['crimes']['neighborhood'].reverse()
            crimes['crimes']['percapita'].reverse()
            collection.insert({ filename: {'neighborhood': crimes['crimes']['neighborhood'], 'percapita': crimes['crimes']['percapita']} })
        elif action == 'recent':
            collection_name = '%s-%s' % (location, action)
            collection = db[collection_name]
            crimes = parse.get_recent_crimes(crime, grep, location, args)
            collection.insert(crimes['crimes'])
        elif action == 'specific':
            collection_name = '%s-%s' % (location, action)
            collection = db[collection_name]
    if verbose:
        print crimes

