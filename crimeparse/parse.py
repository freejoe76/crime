#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Run a query against the crime CSV's
import csv
import operator
import re
from collections import defaultdict, OrderedDict
from optparse import OptionParser
from datetime import datetime, date, timedelta
from fancytext.fancytext import FancyText
from textbarchart import TextBarchart
from printcrimes import *
import argparse
import logging
# The location-specific data
import dicts


class Parse:
    """ class Parse is the lowest-level interface with the crime data CSVs.
        Any question we have for the crime data starts with the Parse class.
        There are two means of outputting the results Parse generates: The 
        command-line, and a python dict. 
        >>> parse = Parse('_input/test')
        >>> parse.crime = 'violent'
        >>> parse.grep = False
        >>> parse.location = 'capitol-hill'
        >>> result = parse.get_specific_crime()
        >>> print result['count'], result['crime']
        1 violent
        """

    def __init__(self, crime_filename, diff = False, options = None):
        """ Initialize the primary vars.
            """
        self.grep = False
        self.verbose = False
        self.diff = diff
        self.set_timespan(None)
        self.location = None

        self.date_field = 'FIRST_OCCURRENCE_DATE'
        self.crime_file = self.open_csv(crime_filename, diff)
        self.crime_filename = crime_filename
        self.options = options

    def set_timespan(self, value):
        """ Set the object's timespan, a tuple of dates.
            >>> parse = Parse('_input/test')
            >>> timespan = parse.set_timespan(['2013-01-08', '2013-11-27'])
            >>> print timespan
            (datetime.date(2013, 1, 8), datetime.date(2013, 11, 27))
            """
        if value == None:
            self.timespan = value
            return value

        # This value is either a str or a datetime object.
        try:
            if type(value[0]) is str:
                timespan = (datetime.date(datetime.strptime(value[0], '%Y-%m-%d')), datetime.date(datetime.strptime(value[1], '%Y-%m-%d')))
            elif type(value[0][0]) is str:
                timespan = (datetime.date(datetime.strptime(value[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(value[0][1], '%Y-%m-%d')))
        except:
            timespan = value
        if self.verbose:
            print "Publishing crimes from %s to %s" % ( timespan[0].month, timespan[1].month )
        self.timespan = timespan
        return self.timespan

    def abstract_keys(self, key):
        """ Take a key, return its CSV equivalent.
            Used so we can use this in more than just Denver crime csv.
            """
        pass

    def get_location_list(self, location_type):
        pass

    def get_location_ranking(self, locations, crime_type):
        pass

    def timeago(self, time=False):
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
            Sometimes datestamps have dashes, sometimes they look completely different. 9/9/2016 9:55:00 AM
            >>> parse = Parse('_input/test')
            >>> test_date = parse.check_datetime('2014-01-08 06:05:04')
            >>> print test_date
            2014-01-08 06:05:04
            """
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                # DATEFORMAT
                return datetime.strptime(value, '%m/%d/%Y %I:%M:%S %p')
            except:
                return False
        return False

    def does_crime_match(self, record, crime_type):
        """ Compares the crime against the fields in the record to see if it matches.
            Possible crime_type's include: parent_category, .....
            Used in get_recent and get_monthly.
            >>> parse = Parse('_input/test')
            >>> crime_type = 'parent_category'
            >>> parse.crime = 'other'
            >>> parse.grep = False
            >>> record = parse.get_row()
            >>> print parse.does_crime_match(record, crime_type)
            True
            """
        if  type(record) is not dict:
            return False
        if crime_type == 'parent_category':
            if record['OFFENSE_CATEGORY_ID'] in dicts.crime_lookup_reverse[self.crime]:
                return True
        else:
            if record[crime_type] == self.crime:
                return True
            elif self.grep == True:
                # Loop through the types of crimes 
                # (the lowest-level crime taxonomy), 
                # looking to match a partial string.
                if '*' in self.crime:
                    search_re = self.crime.replace('*', '.*')
                    if re.search(search_re, record['OFFENSE_TYPE_ID']) != None:
                        return True
                elif self.crime in record['OFFENSE_TYPE_ID']:
                    return True

        return False

    def get_address_type(self):
        """ Distinguish between the types of addresses we may be searching:
            Street address, a street block, or a lat/lon.
            >>> parse = Parse('_input/test')
            >>> parse.address = '39.23,24.00'
            >>> print parse.get_address_type()
            lat/lon
            """
        if ',' in self.address:
            return 'lat/lon'
        elif 'BLK' in self.address:
            return 'block'
        return 'street'

    def get_addresses(self, *args):
        """ Get all the unique addresses. Filterable by neighborhood.
            Returns a dict of streets with unique addresses, and crimes at each
            of the addresses, in regards to a neighborhood or the city.
            >>> parse = Parse('_input/test')
            >>> parse.location = 'west-highland'
            >>> result = parse.get_addresses()
            >>> print result['35TH AVE']['4716 W 35TH AVE'][0]['INCIDENT_ADDRESS']
            4716 W 35TH AVE
            """
        if not args or args[0] == []:
            timespan = False
        else:
            timespan = self.set_timespan(args)
        addresses = {}
        for row in self.crime_file:
            if len(row) < 5:
                continue
            record = dict(zip(dicts.keys, row))
            if self.location != None:
                if record['NEIGHBORHOOD_ID'] != self.location:
                    continue

            # Timespan queries
            if self.timespan:
                ts = self.check_datetime(record[self.date_field])
                if ts == False:
                    continue
                if not self.timespan[0] <= ts.date() <= self.timespan[1]:
                    continue

            # Clean up street name
            if 'BLK' in record['INCIDENT_ADDRESS']:
                record['INCIDENT_ADDRESS'] = string.replace(record['INCIDENT_ADDRESS'], 'BLK', 'BLOCK')

            # We build a dict based on street name.
            # Street name will be the last two words in the address.
            street = ' '.join(record['INCIDENT_ADDRESS'].split(' ')[-2:])
            if street not in addresses:
                addresses[street] = OrderedDict()
            if record['INCIDENT_ADDRESS'] not in addresses[street]:
                addresses[street][record['INCIDENT_ADDRESS']] = []
            addresses[street][record['INCIDENT_ADDRESS']].append(record)
            
        return addresses

    def search_addresses(self, *args):
        """ Find crimes that happened at a particular address.
            The goal here is to allow us to loop through a list of addresses w/
            business names and get a list of recent crimes at local businesses.

            To get the newest crimes happening at places, search latestdiff.
            This method returns a crime object with recent crimes and a count.

            Example: How many crimes have been reported at 338 W 12TH AVE?
            $ ./parse.py --verbose --action search --address "338 W 12TH AVE"

            >>> parse = Parse('_input/test')
            >>> parse.address = '1999 N BROADWAY ST'
            >>> parse.grep = False
            >>> result = parse.search_addresses()
            >>> print result['count'], result['crimes'][0]['OFFENSE_CATEGORY_ID']
            1 all-other-crimes
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

            if type_of in ['street', 'block']:
                if self.grep == True:
                    if '*' in self.address:
                        search_re = self.address.replace('*', '.*')
                        if re.search(search_re, record['INCIDENT_ADDRESS']) != None:
                            crimes.append(record)
                    else:
                        if self.address in record['INCIDENT_ADDRESS']:
                            crimes.append(record)
                else:
                    if self.address == record['INCIDENT_ADDRESS']:
                        crimes.append(record)
            if type_of == 'lat/lon':
                # Assumes lat/lon are split by a comma. If not, an error will
                # be thrown and the user will know they are wrong.
                lat, lon = self.address.split(',')
                if lat in record['GEO_LAT'] and lon in record['GEO_LON']:
                    crimes.append(record)

        return { 'count': len(crimes), 'crimes': crimes }

    def get_specific_crime(self, *args):
        """ Indexes specific crime.
            Example: Hey, among Drug & Alcohol abuses in cap hill, is meth more popular than coke?
            $ ./parse.py --verbose --action specific --crime meth --grep True
            $ ./parse.py --verbose --action specific --crime cocaine --grep True
            
            Returns frequency in csv specified.
            Also returns the # of days since the last crime.

            Args, if they exist, should be two valid date or datetimes, and be
            the timespan's range.
            >>> parse = Parse('_input/test')
            >>> parse.crime = 'violent'
            >>> parse.grep = False
            >>> result = parse.get_specific_crime()
            >>> print result['count'], result['crime']
            36 violent
            """
        if not args or args[0] == []:
            timespan = False
        else:
            timespan = self.set_timespan(args)
        crimes = self.get_recent_crimes()
        count = len(crimes['crimes'])
        last_crime = None
        if count > 0:
            # We don't want the header row... it's possible we should take care of this in get_recent.
            if crimes['crimes'][0]['FIRST_OCCURRENCE_DATE'] == 'FIRST_OCCURRENCE_DATE':
                last_crime = self.check_datetime(crimes['crimes'][1][self.date_field])
            else:
                last_crime = self.check_datetime(crimes['crimes'][0][self.date_field])

        return { 'count': count, 'last_crime': self.timeago(last_crime), 'crime': self.crime }

    def get_recent_crimes(self, *args, **kwargs):
        """ Given a crime genre / cat / type, a location or a timespan, return a list of crimes.
            Timespan is passed as an argument (start, finish)
            !!! the input files aren't listed in order of occurence, so we need to sort.
            >>> parse = Parse('_input/test')
            >>> parse.crime = 'violent'
            >>> result = parse.get_recent_crimes()
            >>> print len(result['crimes'])
            36
            """

        diffs = None
        crimes = []
        crime_type = self.get_crime_type()

        if not args or args[0] == []:
            timespan = None
        else:
            timespan = self.set_timespan(args)

        if self.verbose:
            print "Timespan: %s, location: %s, crime: %s" % (self.timespan, location, crime)

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
                if record['INCIDENT_ID'][0] == '<':
                    record['diff'] = 'ADD'
                    adds += 1
                elif record['INCIDENT_ID'][0] == '>': 
                    record['diff'] = 'REMOVED'
                    removes += 1

                # Strip the "< " at the start, and the ".0" at the end
                record['INCIDENT_ID'] = record['INCIDENT_ID'][2:-2]

            # Timespan queries
            if self.timespan:
                ts = self.check_datetime(record[self.date_field])
                if ts == False:
                    continue
                if not self.timespan[0] <= ts.date() <= self.timespan[1]:
                    continue

            # Location, then crime queries
            # This logic tree is a lot like four shrubs next to each other:
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
            >>> parse.crime = 'violent'
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
            {'OFFENSE_CATEGORY_ID': 'public-disorder', 'INCIDENT_ID': '201796199', 'GEO_X': '3193674', 'REPORTED_DATE': '2/11/2017 11:25:00 AM', 'OFFENSE_CODE': '5309', 'FIRST_OCCURRENCE_DATE': '8/1/2016 7:00:00 AM', 'OFFENSE_CODE_EXTENSION': '0', 'DISTRICT_ID': '5', 'GEO_LAT': '39.77995290', 'LAST_OCCURRENCE_DATE': '2/11/2017 8:00:00 AM', 'OFFENSE_TYPE_ID': 'harassment', 'PRECINCT_ID': '512', 'GEO_Y': '1709713', 'INCIDENT_ADDRESS': '4861 N GRANBY WAY', 'OFFENSE_ID': '201796199530900', 'GEO_LON': '-104.810914', 'NEIGHBORHOOD_ID': 'montbello'}
            """
        record = dict(zip(dicts.keys, self.crime_file[row]))
        return record

    def __contains__(self, item):
        return item in self.__dict__

    def get_monthly(self, limit=12):
        """ Loop through the monthly crime files, return frequency.
            Can filter by crime, location or both. 
            Have some gymnastics to do here in jumping across files.
            Returns a dict of months and # of occurrences.
            >>> parse = Parse('_input/test')
            >>> crime = 'violent'

            # >>> result = parse.get_monthly()
            # >>> print result
            # *** Will need a more robust selection of test data
            """
        i = 0
        crime_type = self.get_crime_type()
        crimes = { 'crime': self.crime, 'counts': dict(), 'max': 0, 'sum': 0, 'avg': 0 }

        # We load year/month strings in like this because the crime data
        # can lag, and we want to be accurate. If the last update of the crime
        # happened two days ago, but that two days ago was a different month,
        # doing it this way keeps it correct.
        yearmonths = open('_input/last.txt').readlines()

        if limit == []:
            limit = 24
        yearmonths = yearmonths[:limit]

        # We need the crimes, the counter, the empty dict, and the month.
        # If we're filtering an existing set of crimes (self.crimes), then we take
        # that instead of the crime file.
        if hasattr(self, 'crimes'):
            crime_file = self.crimes['crimes']
        else:
            if limit > 24:
                filename = 'current'
            else:
                filename = 'last24months'
            crime_file = self.open_csv('_input/%s' % filename, self.diff)

        # Initialize the dict we put the data in, run location search if we have one.
        while i < limit:
            yearmonth = yearmonths[i].strip()
            crimes['counts'][yearmonth] = { 'count': 0, 'date': self.check_date('%s-01' % yearmonth) }

            # Location-specific queries are handled a little different and
            # require slightly different logic.
            if location and not hasattr(self, 'crimes'):
                # Ingests files such as _input/location_capitol-hill-2015-06.csv
                filename = 'location_%s-%s' % (self.location, yearmonth)
                crime_file = self.open_csv('_input/%s' % filename, self.diff)
                if self.crime == None:
                    crimes['counts'][yearmonth]['count'] = len(crime_file)
                else:
                    if not crime_file:
                        crimes['counts'][yearmonth]['count'] = 0
                    else:
                        for row in crime_file:
                            record = dict(zip(dicts.keys, row))
                            if 'OFFENSE_CATEGORY_ID' in row:
                                record = row
                            if self.does_crime_match(record, crime_type):
                                crimes['counts'][yearmonth]['count'] += 1
            i += 1

        if not location:
            for row in crime_file:
                # These two outcomes depend on whether we're reading from a file
                # or already have a dict of crimes that we got from another query.
                record = dict(zip(dicts.keys, row))
                if 'OFFENSE_CATEGORY_ID' in row:
                    record = row

                # We query a more general csv file in the no-location
                # queries, so we have to filter it more.
                if self.does_crime_match(record, crime_type):
                    for yearmonth in yearmonths:
                        ym = yearmonth.strip()
                        bits = ym.split('-')
                        search = re.compile('%s/.*/%s' % (bits[1].lstrip('0'), bits[0]))
                        if search.search(record[self.date_field]):
                            crimes['counts'][ym]['count'] += 1
                            break
                    
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
            If no crime is passed, we rank overall number of crimes
            (and crimes per-capita) in that particular time period.
            The time period defaults to the _input/currentyear.csv.
            Args, if they exist, should be two valid date or datetimes, and be
            the timespan's range.

            We return a dict of raw numbers (dict['crimes']['neighborhood']) 
            and per-capita (dict['crimes']['percapita']) numbers.
            If a location is given, we will also rank all locations.
            >>> parse = Parse('_input/test')
            >>> parse.crime = 'violent'
            >>> result = parse.get_rankings()
            >>> print result['crimes']['neighborhood'][0]
            ('union-station', {'count': 4, 'rank': 0})
            >>> print result['crimes']['percapita'][50]
            ('city-park-west', {'count': 0.0, 'rank': 0})
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
        today = date.today()

        if not args or args[0] == []:
            timespan = False
        else:
            timespan = self.set_timespan(args)

        crime_type = self.get_crime_type()

        for row in self.crime_file:
            record = dict(zip(dicts.keys, row))

            # Sometimes this happens: A header row on the record.
            if record['FIRST_OCCURRENCE_DATE'] == 'FIRST_OCCURRENCE_DATE':
                continue

            # Timespan queries
            if self.timespan:
                ts = self.check_datetime(record[self.date_field])
                if ts == False:
                    # TODO NEED TO SEND THIS TO AN ERROR LOG, NOT STDOUT
                    #print record[self.date_field]
                    pass
                if not self.timespan[0] <= datetime.date(ts) <= self.timespan[1]:
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
                elif self.grep == True:
                    if '*' in self.crime:
                        search_re = self.crime.replace('*', '.*')
                        if re.search(search_re, dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']]) != None or \
                            re.search(search_re, record['OFFENSE_CATEGORY_ID']) != None  or \
                            re.search(search_re, record['OFFENSE_TYPE_ID']) != None:
                            rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                            percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                    else:
                        if self.crime in dicts.crime_lookup[record['OFFENSE_CATEGORY_ID']] or self.crime in record['OFFENSE_CATEGORY_ID'] or self.crime in record['OFFENSE_TYPE_ID']:
                            rankings['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1
                            percapita['neighborhood'][record['NEIGHBORHOOD_ID']]['count'] += 1

        for item in percapita['neighborhood'].items():
            try:
                item[1]['count'] = round( float(item[1]['count'])/float(dicts.populations[item[0]]['2015']) * 1000, 2)
            except:
                #print "ERROR: ", item
                pass

        sorted_rankings = {
            'neighborhood': sorted(rankings['neighborhood'].iteritems(), key=operator.itemgetter(1), reverse=True),
            'percapita': sorted(percapita['neighborhood'].iteritems(), key=operator.itemgetter(1), reverse=True),
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
            set(['OFFENSE_CATEGORY_ID', 'all-other-crimes', 'auto-theft', 'theft-from-motor-vehicle', 'sexual-assault', 'drug-alcohol', 'larceny', 'aggravated-assault', 'other-crimes-against-persons', 'robbery', 'burglary', 'traffic-accident', 'white-collar-crime', 'public-disorder'])
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
        """ Open the crime CSV to parse it.
            It defaults to the current year's file.
            >>> parse = Parse('_input/test')
            >>> result = parse.open_csv('_input/test')
            >>> print result[0][0]
            INCIDENT_ID
            """
        try:
            crime_file_raw = csv.reader(open('%s.csv' % fn, 'rb'), delimiter = ',')
        except:
            return False

        # Sort the csv by the first occurrence (the 7th field, 6 on a 0-index)
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
            >>> parse.crime = 'violent'
            >>> crimes = parse.get_rankings()
            >>> result = parse.print_neighborhoods(crimes)
            >>> print result[0]
                'union-station': {'full': 'Union Station'},
            """
        outputs = []
        for item in crimes['crimes']['percapita']:
            outputs += ["    '%s': {'full': '%s'}," % (item[0], self.clean_location(item[0]))]
            #outputs += ["    '%s': '%s'," % (item[0], item[0])]
        return outputs

def main(args):
    """ What we run when we run this from the command line.
        >>> main(build_parser(None))
        """
    pass

def build_parser(args):
    """ A method to handle argparse.
        >>> args = build_parser(None)
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python parse.py',
                                     description=''' ''',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    return parser.parse_args()

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
    parser.add_option("-m", "--monthly", dest="monthly", default=False, action="store_true")
    parser.add_option("-u", "--unicode", dest="unicode", default=False, action="store_true")
    parser.add_option("-o", "--output", dest="output", default=None)
    parser.add_option("-y", "--yearoveryear", dest="yearoveryear", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_option("-s", "--silent", dest="silent", action="store_true")
    (options, args) = parser.parse_args()
    filename = options.filename
    action = options.action
    output = options.output
    yearoveryear = options.yearoveryear
    silent = options.silent
    monthly = options.monthly

    if options.verbose:
        import doctest
        doctest.testmod(verbose=options.verbose)
    
    if options.diff == True:
        filename = 'latestdiff'

    parse = Parse("_input/%s" % filename, options.diff, options)
    location = parse.get_neighborhood(options.location)

    crimes = None
    parse.grep = options.grep
    limit = int(options.limit)
    parse.limit = limit
    crime = options.crime
    parse.crime = crime
    parse.location = location
    verbose = options.verbose
    parse.verbose = verbose
    address = options.address
    parse.address = address
    parse.diff = options.diff
    if action == 'monthly':
        # Example:
        # $ ./parse.py --action monthly --location capitol-hill --crime violent
        # The limit defaults to 0, but 23 is our go-to number in this report.
        if limit == 0:
            limit = 23
        crimes = parse.get_monthly(limit)
        if verbose:
            print crimes
    elif action == 'rankings':
        # Example:
        # $ ./parse.py --action rankings --crime violent --file 2013 '2013-01-01' '2013-02-01'
        # $ ./parse.py --action rankings --crime dv --grep --file 2013 '2013-01-01' '2013-08-01'
        crimes = parse.get_rankings(args)
        if verbose:
            print crimes
        if not location:
            crimes['crimes']['neighborhood'].reverse()
            crimes['crimes']['percapita'].reverse()
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
        crimes = parse.get_specific_crime(*args)
    elif action == 'search':
        crimes = parse.search_addresses(args)
        if monthly:
            parse.crimes = crimes
            crimes = parse.get_monthly(args)
    elif action == 'by-address':
        crimes = parse.get_addresses(args)
    else:
        print "You must specify one of these actions: monthly, rankings, recent, specific, search, by-address."
    if not silent:
        from printcrimes import *
        printjob = PrintCrimes(crimes, action, parse.crime_filename, limit)
        if monthly:
            printjob.monthly = True
        if action == 'search':
            printjob.address = options.address
        print printjob.print_crimes(location, output)
