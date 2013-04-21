#!/usr/bin/python
# Run a query against the crime CSV's
import os
from optparse import OptionParser
from datetime import datetime, timedelta

# The location-specific data
import dicts

divider='\n=============================================================\n'

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", default="currentyear")
    parser.add_option("-a", "--action", dest="action")
    parser.add_option("-l", "--location", dest="location", default=None)
    parser.add_option("-t", "--limit", dest="limit", default=0)
    parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-g", "--grep", dest="grep", default=False, action="store_true")
    parser.add_option("-d", "--diff", dest="diff", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    (options, args) = parser.parse_args()
    filename = options.filename
    action = options.action
    location = options.location
    limit = int(options.limit)
    crime = options.crime
    grep = options.grep
    diff = options.diff
    verbose = options.verbose

    #location = get_neighborhood(location)

    if verbose:
        print "Options: %s\nArgs: %s" % (options, args)

    if diff == True:
        filename = 'latestdiff'

    if action == 'ticker':
        # Example:
        # $ ./write.py --action rankings --crime violent '2013-01-01' '2013-02-01'
    if action == 'rankings':
        # Example:
        # $ ./write.py --action rankings --crime violent '2013-01-01' '2013-02-01'
        crimes = get_rankings(crime, location, args)
        if verbose:
            print crimes
        crimes['crimes']['neighborhood'].reverse()
        crimes['crimes']['percapita'].reverse()
        #print print_neighborhoods(crimes)
    elif action == 'recent':
        # Example:
        # $ ./write.py --action recent --crime violent --location capitol-hill --output csv
        # $ ./write.py --verbose --action recent --crime drug-alcohol --location capitol-hill --diff
        # $ ./write.py --verbose --action recent --crime drug-alcohol --location capitol-hill
        crimes = get_recent_crimes(crime, grep, location, args)
    elif action == 'specific':
        # Example:
        # $ ./write.py --verbose --action specific --crime drug-alcohol
        # $ ./write.py --verbose --action specific --crime meth --grep True 
        crimes = get_specific_crime(crime, grep, location)
