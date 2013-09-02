#!/usr/bin/env python
# Run a query against the crime CSV's
import os
import csv
import operator
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime, timedelta

# The location-specific data
import dicts

divider='\n=============================================================\n'

def timeago(time=False):
    # Get a datetime object or a int() Epoch timestamp and return a
    # pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    # 'just now', etc
    if time == None:
        return "never"
    
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours"
    if day_diff == 1:
        return "One day"
    return str(day_diff) + " days"

class Parse:

    def __init__(self, crime_filename, diff):
        self.crime_file = self.open_csv(crime_filename, diff)
        self.diff = diff
        self.crime_filename = crime_filename

    def abstract_keys(self, key):
        # Take a key, return its CSV equivalent.
        # Used so we can use this for more than just Denver crime csv.
        pass

    def get_location_list(self, location_type):
        pass

    def get_location_ranking(self, locations, crime_type):
        pass

    def get_timespan_crimes(self, location = None, time_type = 'month', quantity = 'this',  *args, **kwargs):
        # Get crimes from a particular span of time
        pass


    def check_date(self, value):
        # Check a date to see if it's valid. If not, throw error.
        return datetime.strptime(value, '%Y-%m-%d')

    def check_datetime(self, value):
        # Check a datetime to see if it's valid. If not, throw error.
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            print value
            return False

    def does_crime_match(self, crime, grep, record, crime_type):
        # Compares the crime against the fields in the record to see if it matches.
        # Used in get_recent and get_monthly.
        if crime_type == 'parent_category':
            if record['OFFENSE_CATEGORY_ID'] in dicts.crime_lookup_reverse[crime]:
                return True
        else:
            if record[crime_type] == crime:
                return True
            elif grep == True:
                # Loop through the types of crimes 
                # (the lowest-level crime taxonomy), 
                # looking for a partial string match.
                if crime in record['OFFENSE_TYPE_ID']:
                    return True

        return False

    def get_specific_crime(self, crime, grep, location = None):
        # Indexes specific crime.
        # Example: Hey, among Drug & Alcohol abuses in cap hill, is meth more popular than coke?
        # $ ./parse.py --verbose --action specific --crime meth --grep True
        # $ ./parse.py --verbose --action specific --crime cocaine --grep True
        # 
        # Returns frequency for csv specified.
        # Also returns the # of days since the last crime.
        crimes = self.get_recent_crimes(crime, grep, location)
        count = len(crimes['crimes'])
        last_crime = None
        if count > 0:
            last_crime = self.check_datetime(crimes['crimes'][0]['FIRST_OCCURRENCE_DATE'])

        return { 'count': count, 'last_crime': timeago(last_crime), 'crime': crime }

    def get_recent_crimes(self, crime = None, grep = False, location = None, verbose = False, diff = False, *args, **kwargs):
        # Given a crime genre / cat / type, a location or a timespan, return a list of crimes.
        # Timespan is passed as an argument (start, finish)
        # !!! the input files aren't listed in order of occurence, so we need to sort.

        diffs = None
        crimes = []
        crime_type = self.get_crime_type(crime)

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

        for row in self.crime_file:
            if len(row) < 5:
                continue
            record = dict(zip(dicts.keys, row))
            #print record

            # Address diffs, if we've got 'em.
            if diff == True:
                #print record['INCIDENT_ID'][0]
                if record['INCIDENT_ID'][0] == '>':
                    record['diff'] = 'ADD'
                    adds += 1
                elif record['INCIDENT_ID'][0] == '<': 
                    record['diff'] = 'REMOVED'
                    removes += 1

                # Strip the "< " at the start, and the ".0" at the end
                record['INCIDENT_ID'] = record['INCIDENT_ID'][2:-2]

            # Time queries
            if timespan:
                ts = self.check_datetime(record['FIRST_OCCURRENCE_DATE'])
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
                if self.does_crime_match(crime, grep, record, crime_type):
                    crimes.append(record)

        diffs = None
        if diffs == True:
            diffs = { 'adds': adds, 'removes': removes }
        return { 'crimes': crimes, 'diffs': diffs }


    def get_crime_type(self, crime):
        # Figure out what type of crime we're querying
        # parent_category doesn't correspond to a CSV field,
        # which is why it looks different. So that's obvious.
        # type OFFENSE_TYPE_ID
        # genre violent / property / other 
        # category OFFENSE_CATEGORY_ID
        crime_type = 'OFFENSE_TYPE_ID'
        if crime in dicts.crime_genres:
            crime_type = 'parent_category'
        elif crime in dicts.crime_lookup:
            crime_type = 'OFFENSE_CATEGORY_ID'

        return crime_type

    def get_monthly(self, crime = None, grep = False, location = '', limit = 24):
        # Loop through the monthly crime files, return frequency.
        # Can filter by crime, location or both. 
        # Have some gymnastics to do her in jumping across files.
        # Return a dict of months and # of occurrences.
        i = 0
        crime_type = self.get_crime_type(crime)
        crimes = { 'crime': crime, 'counts': dict(), 'max': 0, 'sum': 0 }

        # We load year/month strings in like this because the crime data
        # can lag, and we want to be accurate. If the last update of the crime
        # happened two days ago, but that two days ago was a different month,
        # doing it this way keeps it correct.
        yearmonths = open('_input/last24months.txt').readlines()

        while i < limit:
            # We need the crimes, the counter, the empty dict, and the month.
            yearmonth = yearmonths[i].strip()
            crime_file = self.open_csv('_input/location_%s-%s' % (location, yearmonth))
            i += 1
            crimes['counts'][yearmonth] = { 'count': 0, 'date': self.check_date('%s-01' % yearmonth) }

            if crime == None:
                crimes['counts'][yearmonth]['count'] = len(crime_file)
                continue

            for row in crime_file:
                record = dict(zip(dicts.keys, row))
                if self.does_crime_match(crime, grep, record, crime_type):
                    crimes['counts'][yearmonth]['count'] += 1

            crimes['sum'] += crimes['counts'][yearmonth]['count']

            # Figure out if we need to update the max
            if crimes['counts'][yearmonth]['count'] > crimes['max']:
                crimes['max'] = crimes['counts'][yearmonth]['count']
                    
        return crimes

    def get_rankings(self, crime = None, grep = False, location = None, *args, **kwargs):
        # Take a crime type or category and return a list of neighborhoods 
        # ranked by frequency of that crime.
        # If no crime is passed, we just rank overall number of crimes
        # (and crimes per-capita) for that particular time period.
        # Args taken should be the start of the timespan and the end.
        # We return raw numbers and per-capita numbers.
        # If a location is given, we will also return that location's rank
        # within each list.
        rankings = { 
            'neighborhood': dict(),
            'genre': defaultdict(int),
            'category': defaultdict(int),
            'type': defaultdict(int)
        }
        percapita = { 
            'neighborhood': dict(),
            'genre': defaultdict(int),
            'category': defaultdict(int),
            'type': defaultdict(int)
        }
        percapita_multiplier = 1000
        today = datetime.date(datetime.now())

        if not args or args[0] == []:
            timespan = False
        else:
            timespan = (datetime.date(datetime.strptime(args[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(args[0][1], '%Y-%m-%d')))

        crime_type = self.get_crime_type(crime)

        for row in self.crime_file:
            record = dict(zip(dicts.keys, row))

            # Sometimes this happens. *** What is "this"?
            if record['FIRST_OCCURRENCE_DATE'] == 'FIRST_OCCURRENCE_DATE':
                continue

            # Time queries
            ts = self.check_datetime(record['FIRST_OCCURRENCE_DATE'])
            if timespan != False and not timespan[0] <= datetime.date(ts) <= timespan[1]:
                continue

            # Create the neighborhood dict if we haven't yet:
            if record['NEIGHBORHOOD_ID'] not in rankings['neighborhood']:
                rankings['neighborhood'][record['NEIGHBORHOOD_ID']] = { 'count': 0, 'rank': 0 }
                percapita['neighborhood'][record['NEIGHBORHOOD_ID']] = { 'count': 0, 'rank': 0 }

            if crime == None:
                # Update the neighborhood counter
                rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                rankings['type'][record['OFFENSE_TYPE_ID']] += 1
                rankings['category'][record['OFFENSE_CATEGORY_ID']] += 1
                crime_genre = dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']]
                rankings['genre'][crime_genre] += 1

            else:

                if crime == dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']] or crime == record['OFFENSE_CATEGORY_ID'] or crime == record['OFFENSE_TYPE_ID']:
                    rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                    percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                elif grep == True and crime in dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']] or crime in record['OFFENSE_CATEGORY_ID'] or crime in record['OFFENSE_TYPE_ID']:
                    rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                    percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1

        for item in percapita['neighborhood'].items():
            item[1]['count'] = round( float(item[1]['count'])/float(dicts.populations[item[0]]) * 1000, 2)

        sorted_rankings = {
            'neighborhood': sorted(rankings['neighborhood'].iteritems(), key=operator.itemgetter(1)),
            'percapita': sorted(percapita['neighborhood'].iteritems(), key=operator.itemgetter(1)),
            'genre': sorted(rankings['genre'].iteritems(), key=operator.itemgetter(1)),
            'category': sorted(rankings['category'].iteritems(), key=operator.itemgetter(1)),
            'type': sorted(rankings['type'].iteritems(), key=operator.itemgetter(1))
        }

        if location is not None:
            # Here is where we care about populating the rankings field in the neighborhood dict.
            # There's no reason to look up locations on the command-line client, so
            # the ordering of the dict / lack thereof doesn't matter.
            unsorted_rankings = {
                'neighborhood': dict(sorted_rankings['neighborhood']),
                'percapita': dict(sorted_rankings['percapita'])
            }
            for item in ['neighborhood', 'percapita']:
                rank = 1
                for subitem in unsorted_rankings[item]:
                    unsorted_rankings[item][subitem]['rank'] = rank;
                    rank += 1
            return { 'crimes': unsorted_rankings }
        else:
            return { 'crimes': sorted_rankings }

    def get_median(self, ranking):
        # Take a ranking dict, add up the numbers, get the median.
        pass

    def get_uniques(self, field):
        # Write a list of unique values from a field in the CSV
        values = []
        for row in self.crime_file:
            record = dict(zip(dicts.keys, row))
            values.append(record[field])

        print set(values)
        return set(values)

    def get_neighborhood(self, location):
        # If location's in the list return that location name
        if location in dicts.neighborhoods:
            return location
        return None
        
    def open_csv(self, fn = '_input/currentyear', diff = False):
        # Open the crime file for parsing.
        # It defaults to the current year's file.
        crime_file_raw = csv.reader(open('%s.csv' % fn, 'rb'), delimiter = ',')

        # Sort the csv by the reported date (the 7th field, 6 on a 0-index,
        # because that's the only one that's guaranteed to be in the record.
        # Newest items go on top. It's possible we won't hard-code
        # this forever.
        if diff == False:
            crime_file = sorted(crime_file_raw, key=operator.itemgetter(6), reverse=True)
        else:
            crime_file = crime_file_raw
        return crime_file

    def clean_location(self, location):
        # Take the location string, replace the -'s, capitalize what we can.
        location = location.replace('-', ' ')

        # Locations 3 letters or fewer are probably acronyms, and should be capital.
        if len(location) <= 3:
            return location.upper()

        return location.title()

    def print_neighborhoods(self, crimes):
        # Output a dict of neighborhoods to fancy-names.
        # $ ./parse.py --action rankings --crime violent
        outputs = ''
        for item in crimes['crimes']['percapita']:
            #outputs += "    '%s': {'full': '%s'},\n" % (item[0], clean_location(item[0]))
            outputs += "    '%s': '%s',\n" % (item[0], item[0])
        return outputs

    def print_crimes(self, crimes, limit, action, loc=None, *args):
        # How do we want to display the crimes?
        # Right now we're publishing them to be read in terminal.
        # What we're parsing affects the dicts we have.
        outputs = ''

        if action == 'recent' or action == 'specific':
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

                if 'diff' not in crime:
                    crime['diff'] = ''

                outputs += '''%i. %s %s: %s
        Occurred: %s - %s
        Reported: %s
        %s\n\n''' % (i, crime['diff'], crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['LAST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'])
        elif action == 'rankings':
            outputs += "%sDenver crimes, per-capita:%s\n" % (divider, divider)
            i = 0
            for item in crimes['crimes']['percapita']:
                i = i + 1
                if loc == item[0]:
                    location = '***%s***' % self.clean_location(item[0])
                else:
                    location = self.clean_location(item[0])
                outputs += "%i. %s, %s\n" % (i, location, item[1]['count'])

            outputs += "%sDenver crimes, raw:%s\n" % (divider, divider)
            i = 0
            for item in crimes['crimes']['neighborhood']:
                i = i + 1
                if loc == item[0]:
                    location = '***%s***' % self.clean_location(item[0])
                else:
                    location = self.clean_location(item[0])
                outputs += "%i. %s, %s\n" % (i, location, item[1]['count'])

        elif action == 'specific':
            outputs = '%i %s crimes, last one %s' % ( crimes['count'], crimes['crime'], crimes['last_crime'] )

        elif action == 'monthly':
            crime_dict = list(reversed(sorted(crimes['counts'].iteritems(), key=operator.itemgetter(0))))
            for item in crime_dict:
                values = {
                    'date': datetime.strftime(item[1]['date'], '%b %Y'),
                    'count': item[1]['count'],
                    'barchart': '#'*int(item[1]['count'])
                }
                if crimes['max'] > 80:
                    outputs += '%(date) %(count)\n' % values
                else:
                    outputs += '%(date)s %(barchart)s %(count)s\n' % values

        else:
            print "We did not have any crimes to handle"
            outputs = ''

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
    parser.add_option("-s", "--silent", dest="silent", action="store_true")
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
    silent = options.silent

    
    if verbose:
        print "Options: %s\nArgs: %s" % (options, args)

    if diff == True:
        filename = 'latestdiff'

    parse = Parse("_input/%s" % filename, diff)
    location = parse.get_neighborhood(location)


    crimes = None
    if action == 'monthly':
        # Example:
        # $ ./parse.py --action monthly --location capitol-hill --crime violent
        crimes = parse.get_monthly(crime, grep, location)
        if verbose:
            print crimes
    if action == 'rankings':
        # Example:
        # $ ./parse.py --action rankings --crime violent '2013-01-01' '2013-02-01'
        # $ ./parse.py --action rankings --crime dv --grep '2013-01-01' '2013-08-01'
        crimes = parse.get_rankings(crime, grep, location, args)
        if verbose:
            print crimes
        if not location:
            crimes['crimes']['neighborhood'].reverse()
            crimes['crimes']['percapita'].reverse()
        #print print_neighborhoods(crimes)
    elif action == 'recent':
        # Example:
        # $ ./parse.py --action recent --crime violent --location capitol-hill --output csv
        # $ ./parse.py --action recent --location capitol-hill
        # $ ./parse.py --verbose --action recent --crime drug-alcohol --location capitol-hill --diff
        # $ ./parse.py --verbose --action recent --crime drug-alcohol --location capitol-hill
        crimes = parse.get_recent_crimes(crime, grep, location, args)
    elif action == 'specific':
        # Example:
        # $ ./parse.py --verbose --action specific --crime drug-alcohol
        # $ ./parse.py --verbose --action specific --crime meth --grep
        crimes = parse.get_specific_crime(crime, grep, location)
    if not silent:
        print parse.print_crimes(crimes, limit, action, location)
