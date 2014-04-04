#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Print output from a parsing of the crime CSVs
from optparse import OptionParser
from parse import Parse
from fancytext.fancytext import FancyText
from textbarchart import TextBarchart

class PrintJob:
    """ class PrintJob prints the results of a Parse.
        >>> parse = Parse('_input/test')
        >>> parse.set_crime('violent')
        'violent'
        >>> parse.set_grep(False)
        False
        >>> parse.set_location('capitol-hill')
        'capitol-hill'
        >>> printjob = PrintJob(parse.get_specific_crime(), 'specific', parse.crime_filename)
        >>> results = printjob.print_crimes()
        >>> print results.split(',')[0]
        3 violent crimes
        """
    def __init__(self, crimes = None, action = None, crime_filename = None, limit = 15, diff = False, options = None):
        # Initialize the major vars
        self.set_crimes(crimes)
        self.set_action(action)
        self.crime_filename = crime_filename
        self.set_location(None)
        self.set_limit(None)
        self.set_verbose(None)
        self.set_diff(diff)

        self.options = options

    def set_crimes(self, value):
        """ Set the object's crimes var.
            >>> printjob = PrintJob('_input/test')
            >>> crimes = printjob.set_crimes('love')
            >>> print crimes
            love
            """
        self.crimes = value
        return self.crimes

    def set_action(self, value):
        """ Set the object's action var.
            >>> printjob = PrintJob('_input/test')
            >>> action = printjob.set_action(False)
            >>> print action
            False
            """
        self.action = value
        return self.action

    def set_location(self, value):
        """ Set the object's location var.
            >>> parse = Parse('_input/test')
            >>> location = parse.set_location('cbd')
            >>> print location
            cbd
            """
        self.location = value
        return self.location

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

    #def print_crimes(self, crimes, limit, action, loc=None, output=None, *args):
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
        crimes = self.crimes
        limit = self.limit
        action = self.action

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
        %s
        %s,%s\n\n''' % (i, crime['OFFENSE_CATEGORY_ID'], crime['OFFENSE_TYPE_ID'], crime['FIRST_OCCURRENCE_DATE'], crime['LAST_OCCURRENCE_DATE'], crime['REPORTED_DATE'], crime['INCIDENT_ADDRESS'], crime['GEO_LAT'], crime['GEO_LON'])

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
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()
    import doctest
    doctest.testmod(verbose=options.verbose)
    parse = Parse('_input/test')
    parse.set_crime('violent')
    parse.set_grep(False)
    parse.set_location('capitol-hill')
    result = parse.get_specific_crime()
    printjob = PrintJob(result, 'specific', parse.crime_filename)
    '''
    parse.set_grep(options.grep)
    limit = parse.set_limit(int(options.limit))
    crime = parse.set_crime(options.crime)
    location = parse.set_location(location)
    verbose = parse.set_verbose(options.verbose)
    address = parse.set_address(options.address)
    parse.set_diff(options.diff)
    '''
