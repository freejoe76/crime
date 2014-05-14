#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (month / quarter / year) report.
#
# Takes input (report time type, report location) and returns report in output type desired (json, text)
from optparse import OptionParser
from parse import Parse

class Report:
    """ class Report is an interface with class Parse to pull out defined 
        crime queries ( crime_items ). Report takes a dict of crime_item definitions:
        { '[[slug]]': { 'name': '[[full-name]]', 'options': { 'type': 'month', 'location': 'capitol-hill' } } }
        """

    def __init__(self, date_type, location, numago = 1, output = 'json', options = None):
        # Initialize the major vars
        self.set_date_type(date_type)
        self.set_numago(numago)
        self.set_location(location)
        self.set_output(output)

    def set_date_type(self, value):
        """ Set the object's date_type var.
            >>> report = Report('month', 'capitol-hill')
            >>> date_type = report.set_date_type('quarter')
            >>> print date_type
            quarter
            """
        self.date_type = value
        return self.date_type

    def set_numago(self, value):
        """ Set the object's numago var.
            >>> report = Report('month', 'capitol-hill', 3)
            >>> numago = report.set_numago(1)
            >>> print numago
            1
            """
        self.numago = value
        return self.numago

    def set_location(self, value):
        """ Set the object's location var.
            >>> report = Report('month', 'capitol-hill')
            >>> location = report.set_location('cbd')
            >>> print location
            cbd
            """
        self.location = value
        return self.location

    def set_output(self, value):
        """ Set the object's output var.
            >>> report = Report('month', 'capitol-hill')
            >>> output = report.set_output('text')
            >>> print output
            text
            """
        self.output = value
        return self.output

    """
    # For reference
    SUFFIX="--action rankings --location $LOCATION --output json --file $MONTH"monthsago
    VIOLENT=`./parse.py --crime violent $SUFFIX`
    DV=`./parse.py --crime dv --grep $SUFFIX`
    PROPERTY=`./parse.py --crime property $SUFFIX`
    ROBBERY=`./parse.py --crime robbery --grep $SUFFIX`
    BURGLE=`./parse.py --crime burg --grep $SUFFIX`
    BURGLE_RESIDENCE=`./parse.py --crime burglary-residence --grep $SUFFIX`
    BURGLE_BUSINESS=`./parse.py --crime burglary-business --grep $SUFFIX`
    BURGLE_FORCED=`./parse.py --crime by-force --grep $SUFFIX`
    BURGLE_UNFORCED=`./parse.py --crime no-force --grep $SUFFIX`
    THEFT_CAR=`./parse.py --crime theft-of-motor-vehicle $SUFFIX`
    THEFT_BICYCLE=`./parse.py --crime theft-bicycle $SUFFIX`
    echo '[{' >> $FILENAME
    echo '"violent": '$VIOLENT',' >> $FILENAME
    echo '"dv": '$DV',' >> $FILENAME
    """
    def build_filename(self):
        """ Put together the pieces we need to get the filename we query.
            """
        if self.date_type == 'month':
            return '%smonthsago' % self.numago
        if self.date_type == 'year':
            return ''

    def get_crime_item(self):
        """ Return a Parse report.
            """
        parse = Parse('_input/%s' % self.build_filename)
        parse.set_crime('violent')
        parse.set_grep(False)
        parse.set_location(self.location)
        result = parse.get_rankings()
        print result

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--date_type", dest="date_type")
    parser.add_option("-n", "--numago", dest="numago")
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-o", "--output", dest="output", default="json")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()

    import doctest
    doctest.testmod(verbose=options.verbose)

    report = Report(options.date_type, options.location, options.numago, options.output)
    report.get_crime_item()
