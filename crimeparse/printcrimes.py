#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Print output from a parsing of the crime CSVs
from optparse import OptionParser
from fancytext.fancytext import FancyText
from textbarchart import TextBarchart
from datetime import datetime
import operator
import string
import json

# We only want this module once.
try:
    from parse import Parse
except:
    pass

divider = '\n=============================================================\n'


class PrintCrimes:
    """ class PrintCrimes prints the results of a Parse.
        >>> parse = Parse('_input/test')
        >>> parse.crime = 'violent'
        >>> parse.grep = False
        >>> result = parse.get_specific_crime()
        >>> printcrimes = PrintCrimes(result, 'specific')
        >>> report = printcrimes.print_crimes()
        >>> print report.split(",")[0]
        43 violent crimes
        """

    def __init__(self, crimes, action, limit=15, diff=False, options=None):
        # Initialize the major vars
        self.diff = diff

        self.crimes = crimes
        self.options = options
        self.action = action
        self.monthly = False

    def clean_location(self, location):
        """ Take the location string, replace the -'s, capitalize what we can.
            >>> parse = Parse('_input/test')
            >>> parse.crime = 'violent'
            >>> result = parse.get_recent_crimes()
            >>> printcrimes = PrintCrimes(result, 'specific')
            >>> printcrimes.clean_location('capitol-hill')
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
            >>> result = parse.get_rankings()
            >>> printcrimes = PrintCrimes(result, 'specific')
            >>> neighborhoods = printcrimes.print_neighborhoods(result)
            >>> print neighborhoods[0], len(neighborhoods)
                'sun-valley': {'full': 'Sun Valley'}, 75
            """
        outputs = []
        for item in crimes['crimes']['percapita']:
            outputs += ["    '%s': {'full': '%s'}," % (item[0], self.clean_location(item[0]))]
        return outputs

    # def print_crimes(self, crimes, limit, action, loc=None, output=None, *args):
    def print_crimes(self, loc=None, output=None, *args):
        """ How do we want to display the crimes?
            This method takes a dict of crimes (the type of dict depends on
            which method we chose to piece this together).
            It also takes an action, which corresponds to which type of dict
            we have.
            Possible actions: recent, specific, rankings, monthly.

            Right now we're publishing them to be read in terminal.
            What we're parsing affects the dicts we have.
            >>> parse = Parse('_input/test')
            >>> parse.crime = 'violent'
            >>> result = parse.get_recent_crimes()
            >>> limit, action = 1, 'recent'
            >>> printcrimes = PrintCrimes(result, action, limit)
            >>> report = printcrimes.print_crimes()
            >>> print report.split("\\n")[0]
            1.  aggravated-assault: aggravated-assault-dv
            >>> result = parse.get_specific_crime()
            >>> printcrimes = PrintCrimes(result, 'specific')
            >>> report = printcrimes.print_crimes()
            >>> print report.split(",")[0]
            43 violent crimes

            #>>> crimes = parse.get_rankings('violent')
            #>>> report = parse.print_crimes(crimes, 15, 'rankings')
            #>>> print report
            #1.  aggravated-assault: aggravated-assault-dv
            """
        outputs, json_str = '', None
        crimes = self.crimes
        try:
            limit = self.limit
        except:
            limit = 0
        action = self.action

        if 'crimes' not in crimes and action not in ['search', 'monthly', 'specific', 'by-address']:
            return False

        if action == 'by-address':
            json_str = json.dumps(crimes)

        elif action == 'specific':
            if output == 'json':
                # print self.crime
                # rank_add = self.get_rankings(self.crime, self.grep, loc)
                # print rank_add
                json_str = """{\n    "items": [
    {
    "count": "%(count)i",
    "crime": "%(crime)s",
    "last_crime": "%(last_crime)s"
    }]\n}""" % crimes
            else:
                outputs = '%(count)i %(crime)s crimes, last one %(last_crime)s ago' % crimes

        elif action == 'monthly' or self.monthly:

            # We use the textbarchart here.
            self.options = {'unicode': True}
            options = {
                        'type': None, 'font': 'monospace',
                        'unicode': self.options['unicode']}
            crime_dict = list(reversed(sorted(crimes['counts'].iteritems(),
                              key=operator.itemgetter(0))))
            if output == 'json':
                length = len(crime_dict)
                comma = ','
                i = 0
                json_str = '['
                for item in crime_dict:
                    i += 1
                    if i == length:
                        comma = ''
                    json_str += '\n {"count": "%s", "date": "%s"}%s' % (item[1]['count'], item[0], comma)
                json_str += ']'
            else:
                bar = TextBarchart(options, crime_dict, crimes['max'])
                outputs = bar.build_chart()

        elif action in ['recent', 'search']:
            # Lists, probably recents, with full crime record dicts
            i = 0
            if output == 'csv':
                outputs += 'id, category, type, date_occurred, date_reported, address, neighborhood, lat, lon\n'
            elif output == 'json':
                json_str = '{\n    "items": ['

            crimes_to_print = crimes['crimes'][:limit]
            if limit == 0:
                crimes_to_print = crimes['crimes']
            length = len(crimes_to_print)

            for crime in crimes_to_print:
                i = i + 1

                # Sometimes these "\" get fat-fingered into the address field,
                # which is a problem bc it's an escape character that breaks 
                # python's json library.
                if '\\' in crime['INCIDENT_ADDRESS']:
                    crime['INCIDENT_ADDRESS'] = string.replace(crime['INCIDENT_ADDRESS'], '\\', '')

                # Include the weekday, and a boolean flag for whether it's a weekend day
                d = crime['FIRST_OCCURRENCE_DATE'].split(' ')[0]
                try:
                    weekday = datetime.strptime(d, '%M/%d/%Y').weekday()
                except:
                    weekday = datetime.strptime(d, '%Y-%M-%d').weekday()
                weekend = 0
                if weekday == 0 or weekday == 6:
                    weekend = 1

                # Include the hour.
                # Now that the datetime format's changed we have to account for PM's.
                bits = crime['FIRST_OCCURRENCE_DATE'].split(' ')
                hour = int(bits[1].split(':')[0])
                if bits[2] in ['AM', 'PM']:
                    if bits[2] == 'PM':
                        hour += 12

                if output == 'csv':
                    outputs += '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (crime['INCIDENT_ID'], crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'], crime['NEIGHBORHOOD_ID'], crime['GEO_LAT'], crime['GEO_LON'])
                    # outputs += '%s, %s, %s, %s, %s, %s, %s, %s\n' % (crime['OFFENSE_ID'], crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'], crime['NEIGHBORHOOD_ID'], crime['GEO_LAT'], crime['GEO_LON'])
                    continue
                elif output == 'json':
                    close_bracket = '},'
                    if i == length:
                        close_bracket = '}'

                    json_str += """  {
    "category": "%s",
    "type": "%s",
    "date_reported": "%s",
    "date_occurred": "%s",
    "address": "%s",
    "latitude": "%s",
    "longitude": "%s",
    "neighborhood": "%s",
    "weekday": "%d",
    "weekend": "%d",
    "hour": "%d"
    %s
""" % (crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['REPORTED_DATE'], crime['FIRST_OCCURRENCE_DATE'], crime['INCIDENT_ADDRESS'], crime['GEO_LAT'], crime['GEO_LON'], crime['NEIGHBORHOOD_ID'], weekday, weekend, hour, close_bracket)
                    continue

                if 'diff' not in crime:
                    crime['diff'] = ''

                outputs += '''%i. %s %s: %s
        Occurred: %s - %s
        Reported: %s
        %s\n\n''' % (i, crime['diff'], crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['LAST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'])

            # Tie up loose strings
            if output == 'json':
                json_str += ']\n}'


        # No-location rankings get passed a list of neighborhoods and counts
        # rather than a dict, which means the approach for publishing these
        # in the terminal is different.
        elif action == 'rankings' and loc is None:
            outputs += "%sDenver crimes, per-capita:%s\n" % (divider, divider)

            for i, item in enumerate(reversed(crimes['crimes']['percapita'])):
                location = self.clean_location(item[0])
                outputs += "%i. %s, %s\n" % (i+1, location, item[1]['count'])

            outputs += "%sDenver crimes, raw:%s\n" % (divider, divider)
            for i, item in enumerate(reversed(crimes['crimes']['neighborhood'])):
                location = self.clean_location(item[0])
                outputs += "%i. %s, %s\n" % (i+1, location, item[1]['count'])

        elif action == 'rankings':
            outputs += "%sDenver crimes, per-capita:%s\n" % (divider, divider)

            for i, item in enumerate(reversed(sorted(crimes['crimes']['percapita'].iteritems(), key=operator.itemgetter(1)))):
                if loc == item[0]:
                    location = '***%s***' % self.clean_location(item[0])
                else:
                    location = self.clean_location(item[0])

                if output == 'json' and loc == item[0]:
                        json_str = '{ "percapita": [ "rank": "%i", "location": "%s", "count": "%s" ], ' % (i+1, loc, crimes['crimes']['percapita'][item[0]]['count'])
                outputs += "%i. %s, %s\n" % (i+1, location, crimes['crimes']['percapita'][item[0]]['count'])

            outputs += "%sDenver crimes, raw:%s\n" % (divider, divider)
            for i, item in enumerate(reversed(sorted(crimes['crimes']['neighborhood'].iteritems(), key=operator.itemgetter(1)))):
                if loc == item[0]:
                    location = '***%s***' % self.clean_location(item[0])
                else:
                    location = self.clean_location(item[0])

                if output == 'json' and loc == item[0]:
                    json_str += '\n "raw": [ "rank": "%i", "location": "%s", "count": "%s" ] }' % (i, loc, crimes['crimes']['neighborhood'][item[0]]['count'])
                outputs += "%i. %s, %s\n" % (i+1, location, crimes['crimes']['neighborhood'][item[0]]['count'])

        else:
            print "We did not have any crimes to handle"
            outputs = ''

        if json_str is None:
            return outputs
        return json_str

def main(options, args):
    """ We run this when we run this script from the command line.
        >>> main(None, None)
        """
    parse = Parse('_input/test')
    parse.crime = 'violent'
    parse.grep = False
    parse.location = 'capitol-hill'
    result = parse.get_specific_crime()
    printcrimes = PrintCrimes(result, 'specific')

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true", default=True)
    (options, args) = parser.parse_args()
    import doctest
    doctest.testmod(verbose=options.verbose)
    main(options, args)
    '''
    parse.set_grep(options.grep)
    limit = parse.set_limit(int(options.limit))
    crime = parse.set_crime(options.crime)
    location = parse.set_location(location)
    verbose = parse.set_verbose(options.verbose)
    address = parse.set_address(options.address)
    parse.set_diff(options.diff)
    '''
