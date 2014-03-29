#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Run a query against the crime CSV's
import os
import csv
import operator
import math
from collections import defaultdict, OrderedDict
from optparse import OptionParser
from datetime import datetime, timedelta
from fancytext.fancytext import FancyText
from textbarchart import TextBarchart

# The location-specific data
import dicts

divider='\n=============================================================\n'

def timeago(time=False):
    """ Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
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
    """ class Parse is the lowest-level interface with the crime data CSVs.
        Any question we have for the crime data starts with the Parse class.
        There are two means of outputting the results Parse generates: The 
        command-line, and a python dict. 
        >>> parse = Parse('_input/test')
        >>> parse.set_crime('violent')
        'violent'
        >>> parse.set_grep(False)
        False
        >>> parse.set_location('capitol-hill')
        'capitol-hill'
        >>> result = parse.get_specific_crime()
        >>> print result['count'], result['crime']
        3 violent
        """
    def __init__(self, crime_filename, diff = False, options = None):
        # Initialize the major vars
        self.set_crime(None)
        self.set_grep(None)
        self.set_location(None)
        self.set_limit(None)
        self.set_verbose(None)
        self.set_diff(diff)

        self.crime_file = self.open_csv(crime_filename, diff)
        self.crime_filename = crime_filename
        self.options = options

    def set_crime(self, value):
        """ Set the object's crime var.
            >>> parse = Parse('_input/test')
            >>> crime = parse.set_crime('love')
            >>> print crime
            love
            """
        self.crime = value
        return self.crime

    def set_grep(self, value):
        """ Set the object's grep var.
            >>> parse = Parse('_input/test')
            >>> grep = parse.set_grep(False)
            >>> print grep
            False
            """
        self.grep = value
        return self.grep

    def set_location(self, value):
        """ Set the object's location var.
            >>> parse = Parse('_input/test')
            >>> location = parse.set_location('cbd')
            >>> print location
            cbd
            """
        self.location = value
        return self.location

    def set_address(self, value):
        """ Set the object's address var.
            >>> parse = Parse('_input/test')
            >>> address = parse.set_location('835 E 18TH AVE')
            >>> print address
            835 E 18TH AVE
            """
        self.address = value
        return self.address

    def set_limit(self, value):
        """ Set the object's limit var.
            >>> parse = Parse('_input/test')
            >>> limit = parse.set_limit(15)
            >>> print limit
            15
            """
        self.limit = value
        return self.limit

    def set_verbose(self, value):
        """ Set the object's verbose var.
            >>> parse = Parse('_input/test')
            >>> verbose = parse.set_verbose(False)
            >>> print verbose
            False
            """
        self.verbose = value 
        return self.verbose

    def set_diff(self, value):
        """ Set the object's diff var.
            >>> parse = Parse('_input/test')
            >>> diff = parse.set_diff(False)
            >>> print diff
            False
            """
        self.diff = value 
        return self.diff

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
        """ Check a date to see if it's valid. If not, throw error.
            >>> parse = Parse('_input/test')
            >>> test_date = parse.check_date('2014-01-08')
            >>> print test_date
            2014-01-08 00:00:00
            """
        return datetime.strptime(value, '%Y-%m-%d')

    def check_datetime(self, value):
        """ Check a datetime to see if it's valid. If not, return False.
            >>> parse = Parse('_input/test')
            >>> test_date = parse.check_datetime('2014-01-08 06:05:04')
            >>> print test_date
            2014-01-08 06:05:04
            """
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            return False

    def does_crime_match(self, record, crime_type):
        """ Compares the crime against the fields in the record to see if it matches.
            Possible crime_type's include: parent_category, .....
            Used in get_recent and get_monthly.
            >>> parse = Parse('_input/test')
            >>> crime, grep, crime_type = parse.set_crime('property'), parse.set_grep(False), 'parent_category'
            >>> record = parse.get_row()
            >>> print parse.does_crime_match(record, crime_type)
            True
            """
        if crime_type == 'parent_category':
            if record['OFFENSE_CATEGORY_ID'] in dicts.crime_lookup_reverse[self.crime]:
                return True
        else:
            if record[crime_type] == self.crime:
                return True
            elif self.grep == True:
                # Loop through the types of crimes 
                # (the lowest-level crime taxonomy), 
                # looking for a partial string match.
                if self.crime in record['OFFENSE_TYPE_ID']:
                    return True

        return False

    def get_address_type(self):
        """ Distinguish between the types of addresses we may be searching:
            Street address, a street block, or a lat/lon.
            >>> parse = Parse('_input/test')
            >>> address = parse.set_address('39.23,24.00')
            >>> print parse.get_address_type()
            lat/lon
            """
        if ',' in self.address:
            return 'lat/lon'
        elif 'BLK' in self.address:
            return 'block'
        return 'street'

    def search_addresses(self):
        """ Searches crimes for those that happened at a particular address.
            The goal here is to allow us to loop through a list of addresses w/
            business names and get a list of recent crimes at local businesses.

            To get the newest crimes happening at places, search latestdiff.
            This method returns a crime object with recent crimes and a count.

            Example: How many crimes have been reported at 338 W 12TH AVE?
            $ ./parse.py --verbose --action search --address "338 W 12TH AVE"

            >>> parse = Parse('_input/test')
            >>> address, grep = parse.set_address('1999 N BROADWAY ST'), parse.set_grep(False)
            >>> result = parse.search_addresses()
            >>> print result['count'], result['crimes'][0]['OFFENSE_CATEGORY_ID']
            1 public-disorder
            """
        type_of = self.get_address_type()
        crimes = []
        for row in self.crime_file:
            if len(row) < 5:
                continue
            record = dict(zip(dicts.keys, row))
            # Skip removed records on the diff-search
            if self.diff == True:
                if record['INCIDENT_ID'][0] == '<':
                    continue

            if type_of == 'street' or type_of == 'block':
                if self.grep == True:
                    if self.address in record['INCIDENT_ADDRESS']:
                        crimes.append(record)
                else:
                    if self.address = record['INCIDENT_ADDRESS']:
                        crimes.append(record)

        return { 'count': len(crimes), 'crimes': crimes }

    def get_specific_crime(self):
        """ Indexes specific crime.
            Example: Hey, among Drug & Alcohol abuses in cap hill, is meth more popular than coke?
            $ ./parse.py --verbose --action specific --crime meth --grep True
            $ ./parse.py --verbose --action specific --crime cocaine --grep True
            
            Returns frequency for csv specified.
            Also returns the # of days since the last crime.
            >>> parse = Parse('_input/test')
            >>> crime, grep = parse.set_crime('violent'), parse.set_grep(False)
            >>> result = parse.get_specific_crime()
            >>> print result['count'], result['crime']
            43 violent
            """
        crimes = self.get_recent_crimes()
        count = len(crimes['crimes'])
        last_crime = None
        if count > 0:
            # We don't want the header row... it's possible we should take care of this in get_recent.
            if crimes['crimes'][0]['FIRST_OCCURRENCE_DATE'] == 'FIRST_OCCURRENCE_DATE':
                last_crime = self.check_datetime(crimes['crimes'][1]['FIRST_OCCURRENCE_DATE'])
            else:
                last_crime = self.check_datetime(crimes['crimes'][0]['FIRST_OCCURRENCE_DATE'])

        return { 'count': count, 'last_crime': timeago(last_crime), 'crime': self.crime }

    def get_recent_crimes(self, *args, **kwargs):
        """ Given a crime genre / cat / type, a location or a timespan, return a list of crimes.
            Timespan is passed as an argument (start, finish)
            !!! the input files aren't listed in order of occurence, so we need to sort.
            >>> parse = Parse('_input/test')
            >>> parse.set_crime('violent')
            'violent'
            >>> result = parse.get_recent_crimes()
            >>> print len(result['crimes'])
            43
            """

        diffs = None
        crimes = []
        crime_type = self.get_crime_type()

        if not args or args[0] == []:
            timespan = None
        else:
            # timespan a tuple of dates, that defaults to everything.
            # Decided to set that here rather than in the method def for the sake of space.
            timespan = (datetime.date(datetime.strptime(args[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(args[0][1], '%Y-%m-%d')))
            if self.verbose:
                print "Publishing crimes from %s to %s" % ( timespan[0].month, timespan[1].month )

        if self.verbose:
            print "Timespan: %s, location: %s, crime: %s" % (timespan, location, crime)

        if self.diff == True:
            adds = 0
            removes = 0

        for row in self.crime_file:
            if len(row) < 5:
                continue
            record = dict(zip(dicts.keys, row))

            # Address diffs, if we've got 'em.
            if self.diff == True:
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
            if self.location == None and self.crime == None:
                crimes.append(record)
                continue

            if self.location != None:
                if record['NEIGHBORHOOD_ID'] != self.location:
                    continue

            if self.crime == None:
                crimes.append(record)
                continue

            if self.crime != None:
                if self.does_crime_match(record, crime_type):
                    crimes.append(record)

        diffs = None
        if self.diff == True:
            diffs = { 'adds': adds, 'removes': removes }
        return { 'crimes': crimes, 'diffs': diffs }


    def get_crime_type(self):
        """ Figure out which type of crime we're querying.
            parent_category doesn't correspond to a CSV field, which is why 
            it looks different. So that's obvious.
            
            Generally speaking:
                type => OFFENSE_TYPE_ID
                genre => violent / property / other 
                category => OFFENSE_CATEGORY_ID
            >>> parse = Parse('_input/test')
            >>> crime = parse.set_crime('violent')
            >>> result = parse.get_crime_type()
            >>> print result
            parent_category
            """
        crime_type = 'OFFENSE_TYPE_ID'
        if self.crime in dicts.crime_genres:
            crime_type = 'parent_category'
        elif self.crime in dicts.crime_lookup:
            crime_type = 'OFFENSE_CATEGORY_ID'

        return crime_type

    def get_row(self, row=1):
        """ Return a dict of a row from crime_file. Defaults to the first.
            >>> parse = Parse('_input/test')
            >>> print parse.get_row(1)
            {'OFFENSE_CATEGORY_ID': 'theft-from-motor-vehicle', 'INCIDENT_ID': '2008237352.0', 'GEO_X': '3145301.0', 'REPORTED_DATE': '2008-12-23 07:51:59', 'OFFENSE_CODE': '2305', 'FIRST_OCCURRENCE_DATE': '2008-12-22 21:59:59', 'OFFENSE_CODE_EXTENSION': '0', 'DISTRICT_ID': '3', 'GEO_LAT': '39.7005626', 'LAST_OCCURRENCE_DATE': '2008-12-23 06:45:00', 'OFFENSE_TYPE_ID': 'theft-items-from-vehicle', 'PRECINCT_ID': '311', 'GEO_Y': '1680472.0', 'INCIDENT_ADDRESS': '876 S GRANT ST', 'OFFENSE_ID': '2008237352230500', 'GEO_LON': '-104.9836106', 'NEIGHBORHOOD_ID': 'washington-park-west'}
            """
        record = dict(zip(dicts.keys, self.crime_file[row]))
        return record

    def get_monthly(self, limit=24):
        """ Loop through the monthly crime files, return frequency.
            Can filter by crime, location or both. 
            Have some gymnastics to do here in jumping across files.
            Returns a dict of months and # of occurrences.
            >>> parse = Parse('_input/test')
            >>> crime = 'violent'

            # >>> result = parse.get_monthly()
            # >>> print result
            # *** Will need a more robust selection of test data for this one.
            """
        i = 0
        crime_type = self.get_crime_type()
        crimes = { 'crime': self.crime, 'counts': dict(), 'max': 0, 'sum': 0, 'avg': 0 }

        # We load year/month strings in like this because the crime data
        # can lag, and we want to be accurate. If the last update of the crime
        # happened two days ago, but that two days ago was a different month,
        # doing it this way keeps it correct.
        yearmonths = open('_input/last%imonths.txt' % limit).readlines()

        while i < limit:
            # We need the crimes, the counter, the empty dict, and the month.
            yearmonth = yearmonths[i].strip()
            if location:
                filename = 'location_%s-%s' % (self.location, yearmonth)
            else:
                filename = 'last%imonths' % i
            crime_file = self.open_csv('_input/%s' % filename, self.diff)
            i += 1
            crimes['counts'][yearmonth] = { 'count': 0, 'date': self.check_date('%s-01' % yearmonth) }

            if self.crime == None:
                crimes['counts'][yearmonth]['count'] = len(crime_file)
                continue

            for row in crime_file:
                record = dict(zip(dicts.keys, row))
                if self.does_crime_match(record, crime_type):
                    crimes['counts'][yearmonth]['count'] += 1
                    
        # Update the max, sum and avg:
        for item in crimes['counts']:
            crimes['sum'] += crimes['counts'][item]['count']
            if crimes['max'] < crimes['counts'][item]['count']:
                crimes['max'] = crimes['counts'][item]['count']
        crimes['avg'] = crimes['sum'] / len(crimes['counts'])
        return crimes

    def get_rankings(self, *args, **kwargs):
        """ Take a crime type or category and return a list of neighborhoods 
            ranked by frequency of that crime.
            If no crime is passed, we just rank overall number of crimes
            (and crimes per-capita) for that particular time period.
            The time period defaults to the _input/currentyear.csv.
            Args, if they exist, should be two valid date or datetimes, and be
            the timespan's range.

            We return a dict of raw numbers (dict['crimes']['neighborhood']) 
            and per-capita (dict['crimes']['percapita']) numbers.
            If a location is given, we will also rank all locations.

            This is done implicitly in the CLI report. <-- what does that mean?
            >>> parse = Parse('_input/test')
            >>> crime = parse.set_crime('violent')
            >>> result = parse.get_rankings()
            >>> print result['crimes']['neighborhood'][0]
            ('wellshire', {'count': 0, 'rank': 0})
            >>> print result['crimes']['percapita'][50]
            ('west-colfax', {'count': 0.1, 'rank': 0})
            """
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

        crime_type = self.get_crime_type()

        for row in self.crime_file:
            record = dict(zip(dicts.keys, row))

            # Sometimes this happens: A header row on the record.
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

            if self.crime == None:
                # Update the neighborhood counter
                rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                rankings['type'][record['OFFENSE_TYPE_ID']] += 1
                rankings['category'][record['OFFENSE_CATEGORY_ID']] += 1
                crime_genre = dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']]
                rankings['genre'][crime_genre] += 1

            else:

                if self.crime == dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']] or self.crime == record['OFFENSE_CATEGORY_ID'] or self.crime == record['OFFENSE_TYPE_ID']:
                    rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                    percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                elif self.grep == True and self.crime in dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']] or self.crime in record['OFFENSE_CATEGORY_ID'] or self.crime in record['OFFENSE_TYPE_ID']:
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

        if self.location is None:
            return { 'crimes': sorted_rankings }
        else:
            # Here is where we care about populating the rankings field in the neighborhood dict.
            # There's no reason to look up locations on the command-line client, so
            # the ordering of the dict / lack thereof doesn't matter.
            unsorted_rankings = {
                'neighborhood': dict(sorted_rankings['neighborhood']),
                'percapita': dict(sorted_rankings['percapita'])
            }
            for item in ['neighborhood', 'percapita']:
                rank = 1
                for subitem in sorted_rankings[item]:
                    unsorted_rankings[item][subitem[0]]['rank'] = rank
                    rank += 1
            return { 'crimes': unsorted_rankings }

    def get_median(self, ranking):
        """ Take a ranking dict, add up the numbers, get the median.
            """
        pass

    def get_uniques(self, field, print_it=False):
        """ Write a list of unique values from a field in the CSV.
            >>> parse = Parse('_input/test')
            >>> field = 'OFFENSE_CATEGORY_ID'
            >>> parse.get_uniques(field)
            set(['OFFENSE_CATEGORY_ID', 'all-other-crimes', 'murder', 'arson', 'theft-from-motor-vehicle', 'auto-theft', 'sexual-assault', 'drug-alcohol', 'larceny', 'aggravated-assault', 'other-crimes-against-persons', 'robbery', 'burglary', 'white-collar-crime', 'public-disorder'])
            """
        values = []
        for row in self.crime_file:
            record = dict(zip(dicts.keys, row))
            values.append(record[field])

        if print_it is True:
            print set(values)
        return set(values)

    def get_neighborhood(self, location):
        """ If location's in the list then return that location name.
            >>> parse = Parse('_input/test')
            >>> parse.get_neighborhood('capitol-hill')
            'capitol-hill'
            >>> parse.get_neighborhood('elvis-presley')
            
            """
        if location in dicts.neighborhoods:
            return location
        return None
        
    def open_csv(self, fn = '_input/currentyear', diff = False):
        """ Open the crime CSV for parsing.
            It defaults to the current year's file.
            >>> parse = Parse('_input/test')
            >>> result = parse.open_csv('_input/test')
            >>> print result[0][0]
            INCIDENT_ID
            """
        crime_file_raw = csv.reader(open('%s.csv' % fn, 'rb'), delimiter = ',')

        # Sort the csv by the reported date (the 7th field, 6 on a 0-index,
        # because that's the only one that's guaranteed to be in the record.)
        # Newest items go on top. It's possible we won't hard-code
        # this forever.
        if diff == False:
            crime_file = sorted(crime_file_raw, key=operator.itemgetter(6), reverse=True)
        else:
            crime_file = crime_file_raw
        return crime_file

    def clean_location(self, location):
        """ Take the location string, replace the -'s, capitalize what we can.
            >>> parse = Parse('_input/test')
            >>> parse.clean_location('capitol-hill')
            'Capitol Hill'
            """
        location = location.replace('-', ' ')

        # Locations 3 letters or fewer are probably acronyms, and should be capital.
        if len(location) <= 3:
            return location.upper()

        return location.title()

    def print_neighborhoods(self, crimes):
        """ Output a dict of neighborhoods to fancy-names.
            Takes a dict of crimes, as returned by get_rankings.
            
            This is a helper function to build some of the more
            manual dicts in dicts.py
            >>> parse = Parse('_input/test')
            >>> crime = parse.set_crime('violent')
            >>> crimes = parse.get_rankings()
            >>> result = parse.print_neighborhoods(crimes)
            >>> print result[0]
                'wellshire': {'full': 'Wellshire'},
            """
        outputs = []
        for item in crimes['crimes']['percapita']:
            outputs += ["    '%s': {'full': '%s'}," % (item[0], self.clean_location(item[0]))]
            #outputs += ["    '%s': '%s'," % (item[0], item[0])]
        return outputs

    def print_crimes(self, crimes, limit, action, loc=None, output=None, *args):
        """ How do we want to display the crimes?
            This method takes a dict of crimes (the type of dict depends on 
            which method we chose to piece this together).
            It also takes an action, which corresponds to which type of dict
            we have.
            Possible actions: recent, specific, rankings, monthly.

            Right now we're publishing them to be read in terminal.
            What we're parsing affects the dicts we have.
            >>> parse = Parse('_input/test')
            >>> parse.set_crime('violent')
            'violent'
            >>> crimes = parse.get_recent_crimes()
            >>> limit, action = 1, 'recent'
            >>> report = parse.print_crimes(crimes, limit, action)
            >>> print report.split("\\n")[0]
            1.  aggravated-assault: aggravated-assault-dv
            >>> crime, grep = parse.set_crime('violent'), parse.set_grep(False)
            >>> crimes = parse.get_specific_crime()
            >>> report = parse.print_crimes(crimes, limit, 'specific')
            >>> print report.split(",")[0]
            43 violent crimes

            #>>> crimes = parse.get_rankings('violent')
            #>>> report = parse.print_crimes(crimes, 15, 'rankings')
            #>>> print report
            #1.  aggravated-assault: aggravated-assault-dv
            """
        outputs, json = '', None

        if 'crimes' not in crimes and action != 'monthly' and action != 'specific':
            return False

        if action == 'search':
            outputs = '%i crimes at %s.\n' % ( crimes['count'], self.address )
            i = 0
            for crime in crimes['crimes']:
                i = i + 1
                #print crime
                #if 'diff' not in crime:
                #    crime['diff'] = ''

                outputs += '''%i. %s: %s
        Occurred: %s - %s
        Reported: %s
        %s\n\n''' % (i, crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['LAST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'])

        elif action == 'specific':
            if output == 'json':
                #print self.crime
                #rank_add = self.get_rankings(self.crime, self.grep, loc)
                #print rank_add
                json = """{\n    "items": [
    {
    "count": "%i",
    "crime": "%s",
    "filename": "%s",
    "last_crime": "%s"
    }]\n}""" % ( crimes['count'], crimes['crime'], self.crime_filename, crimes['last_crime'] )
            else:
                outputs = '%i %s crimes, (in file %s) last one %s ago' % ( crimes['count'], crimes['crime'], self.crime_filename, crimes['last_crime'] )

        elif action == 'recent':
            # Lists, probably recents, with full crime record dicts
            i = 0
            if output == 'csv':
                outputs += 'category, type, date_reported, address, lat, lon\n'
            elif output == 'json':
                json = '{\n    "items": ['

            crimes_to_print = crimes['crimes'][:limit]
            if limit == 0:
                crimes_to_print = crimes['crimes']
            length = len(crimes_to_print)

            for crime in crimes_to_print:
                i = i + 1
                if output == 'csv':
                    outputs += '%s, %s, %s, %s, %s, %s\n' % (crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'], crime['GEO_LAT'], crime['GEO_LON'])
                    continue
                elif output == 'json':
                    close_bracket = '},'
                    if i == length:
                        close_bracket = '}'

                    json += """  {
    "category": "%s",
    "type": "%s",
    "date-reported": "%s",
    "address": "%s",
    "latitude": "%s",
    "longitude": "%s"
    %s
""" % (crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'], crime['GEO_LAT'], crime['GEO_LON'], close_bracket)
                    continue

                if 'diff' not in crime:
                    crime['diff'] = ''

                outputs += '''%i. %s %s: %s
        Occurred: %s - %s
        Reported: %s
        %s\n\n''' % (i, crime['diff'], crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['LAST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'])

            #if output == 'json':
            #    outputs += ']\n}'


        # No-location rankings get passed a list of neighborhoods and counts
        # rather than a dict, which means the approach for publishing these
        # in the terminal is different.
        elif action == 'rankings' and loc is None:
            outputs += "%sDenver crimes, per-capita:%s\n" % (divider, divider)
            i = 0
            
            for item in crimes['crimes']['percapita']:
                i = i + 1
                location = self.clean_location(item[0])
                outputs += "%i. %s, %s\n" % (i, location, item[1]['count'])

            outputs += "%sDenver crimes, raw:%s\n" % (divider, divider)
            i = 0
            for item in crimes['crimes']['neighborhood']:
                i = i + 1
                location = self.clean_location(item[0])
                outputs += "%i. %s, %s\n" % (i, location, item[1]['count'])

        elif action == 'rankings':
            outputs += "%sDenver crimes, per-capita:%s\n" % (divider, divider)
            i = 0
            
            for item in reversed(sorted(crimes['crimes']['percapita'].iteritems(), key=operator.itemgetter(1))):
                i = i + 1
                if loc == item[0]:
                    location = '***%s***' % self.clean_location(item[0])
                else:
                    location = self.clean_location(item[0])

                if output == 'json' and loc == item[0]:
                        json = '{ "percapita": [ "rank": "%i", "location": "%s", "count": "%s" ], ' % ( i, loc, crimes['crimes']['percapita'][item[0]]['count'] )
                outputs += "%i. %s, %s\n" % (i, location, crimes['crimes']['percapita'][item[0]]['count'])

            outputs += "%sDenver crimes, raw:%s\n" % (divider, divider)
            i = 0
            for item in reversed(sorted(crimes['crimes']['neighborhood'].iteritems(), key=operator.itemgetter(1))):
                i = i + 1
                if loc == item[0]:
                    location = '***%s***' % self.clean_location(item[0])
                else:
                    location = self.clean_location(item[0])

                if output == 'json' and loc == item[0]:
                    json += '\n "raw": [ "rank": "%i", "location": "%s", "count": "%s" ] }' % ( i, loc, crimes['crimes']['neighborhood'][item[0]]['count'] )
                outputs += "%i. %s, %s\n" % (i, location, crimes['crimes']['neighborhood'][item[0]]['count'])

        elif action == 'monthly':
            # We use the textbarchart here.
            options = { 'type': None, 'font': 'monospace', 'unicode': self.options.unicode }
            crime_dict = list(reversed(sorted(crimes['counts'].iteritems(), key=operator.itemgetter(0))))
            bar = TextBarchart(options, crime_dict, crimes['max'])
            outputs = bar.build_chart()
            '''
            divisor = 1
            if crimes['max'] > 80:
                divisor = 50
            if crimes['max'] > 800:
                divisor = 500
            if crimes['max'] > 8000:
                divisor = 5000

            # Calculate the standard deviation.
            # If the deviation's too low, there's no point in publishing the bar part of this chart.
            count = []
            for item in crime_dict:
                count.append(item[1]['count'])
            mean = int(sum(count)/len(count))
            #print mean
            count = []
            for item in crime_dict:
                diff = item[1]['count'] - mean
                count.append(diff*diff)
            variance = int(sum(count)/len(count))
            #print variance
            deviation = int(math.sqrt(variance))

            # *** Possible barchars: #,■,▮
            barchar = '#'
            if self.options.unicode == True:
                barchar = u'■'
                # In case we want the date monospaced.
                font = FancyText()

            # If the deviation-to-mean ratio is more than 50%, that means
            # most of the values are close to the mean and we don't really
            # need a barchart.
            if float(deviation)/mean > .5:
                barchar = ''

            # *** We should have an option to allow for the year if we want it in this month-to-month
            date_format = '%b'

            for item in crime_dict:
                date = datetime.strftime(item[1]['date'], date_format).upper()
                if self.options.unicode == True:
                    date = font.translate(date)
                values = {
                    'date': date,
                    'count': item[1]['count'],
                    'barchart': barchar*int(item[1]['count']/divisor)
                }
                outputs += u'%(date)s %(barchart)s %(count)s\n' % values
            '''

        else:
            print "We did not have any crimes to handle"
            outputs = ''


        # Close up loose strings
        if action == 'recent' and output == 'json':
            json += ']\n}'

        if json is None:
            return outputs
        return json



if __name__ == '__main__':
    # Parse the arguments, pass 'em to the function
    # The three main args we use to query the crime data are
    # location, crime and timespan. location and crime are
    # passed as options, and timespan (start, finish) as the 
    # first two arguments. This may not be the best way to do it.
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", default="currentyear")
    parser.add_option("-a", "--action", dest="action")
    parser.add_option("--address", dest="address")
    parser.add_option("-l", "--location", dest="location", default=None)
    parser.add_option("-t", "--limit", dest="limit", default=0)
    parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-g", "--grep", dest="grep", default=False, action="store_true")
    parser.add_option("-d", "--diff", dest="diff", default=False, action="store_true")
    parser.add_option("-u", "--unicode", dest="unicode", default=False, action="store_true")
    parser.add_option("-o", "--output", dest="output", default=None)
    parser.add_option("-y", "--yearoveryear", dest="yearoveryear", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_option("-s", "--silent", dest="silent", action="store_true")
    (options, args) = parser.parse_args()
    filename = options.filename
    action = options.action
    output = options.output
    yearoveryear = options.yearoveryear
    silent = options.silent

    import doctest
    doctest.testmod(verbose=options.verbose)
    
    if options.diff == True:
        filename = 'latestdiff'

    parse = Parse("_input/%s" % filename, options.diff, options)
    location = parse.get_neighborhood(options.location)

    crimes = None
    parse.set_grep(options.grep)
    limit = parse.set_limit(int(options.limit))
    crime = parse.set_crime(options.crime)
    location = parse.set_location(location)
    verbose = parse.set_verbose(options.verbose)
    address = parse.set_address(options.address)
    parse.set_diff(options.diff)
    if action == 'monthly':
        # Example:
        # $ ./parse.py --action monthly --location capitol-hill --crime violent
        # The limit defaults to 0, but 48 is our go-to number for this report.
        if limit == 0:
            limit = 48
        crimes = parse.get_monthly(limit)
        if verbose:
            print crimes
    elif action == 'rankings':
        # Example:
        # $ ./parse.py --action rankings --crime violent '2013-01-01' '2013-02-01'
        # $ ./parse.py --action rankings --crime dv --grep '2013-01-01' '2013-08-01'
        crimes = parse.get_rankings(args)
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
        crimes = parse.get_recent_crimes(args)
    elif action == 'specific':
        # Example:
        # $ ./parse.py --verbose --action specific --crime drug-alcohol
        # $ ./parse.py --verbose --action specific --crime meth --grep
        crimes = parse.get_specific_crime()
    elif action == 'search':
        crimes = parse.search_addresses()
    else:
        print "You must specify one of these actions: rankings, recent, specific, search."
    if not silent:
        print parse.print_crimes(crimes, limit, action, location, output)
