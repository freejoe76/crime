#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (month / quarter / year) report. A higher-level interface to parse.py
#
# Takes input (report date type, crime, location) and returns report in output type desired (json, text)
from optparse import OptionParser
from parse import Parse

class Report:
    """ class Report is an interface with class Parse to pull out defined 
        crime queries ( crime_items ). Report takes a dict of crime_item definitions:
        { '[[slug]]': { 'name': '[[full-name]]', 'options': { 'type': 'month', 'location': 'capitol-hill', 'crime': 'violent', 'grep': False } } }
        """

    #def __init__(self, date_type='month', location='', numago = 1, output = 'json', options = None, **kwargs):
    def __init__(self, **kwargs):
        # Initialize the major vars
        self.set_date_type(None)
        self.set_location(None)
        self.set_numago(None)
        for key, value in kwargs.iteritems():
            for subkey, subvalue in kwargs[key]['options'].iteritems():
                print subkey, subvalue
                if subkey == 'type':
                    self.set_date_type(subvalue)
                elif subkey == 'location' and subvalue != '':
                    self.set_location(subvalue)
                elif subkey == 'output':
                    self.set_output(subvalue)
                elif subkey == 'crime':
                    self.set_crime(subvalue)
                elif subkey == 'grep':
                    self.set_grep(subvalue)

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

    def set_crime(self, value):
        """ Set the object's crime var.
            >>> report = Report('month', 'capitol-hill')
            >>> crime = report.set_crime('property')
            >>> print crime
            property
            """
        self.crime = value
        return self.crime

    def set_grep(self, value):
        """ Set the object's grep var.
            >>> report = Report('month', 'capitol-hill')
            >>> grep = report.set_grep('True')
            >>> print grep
            True
            """
        self.grep = value
        if value == 'True':
            self.grep = True
        elif value == 'False':
            self.grep = False
        return self.crime

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

    def build_filename(self):
        """ Put together the pieces we need to get the filename we query.
            >>> report = Report('month', 'capitol-hill')
            >>> filename = report.build_filename()
            >>> print filename
            1monthsago
            """
        if self.numago == None:
            self.set_numago(1)

        if self.date_type == 'test':
            return 'test'
        if self.date_type == 'month':
            return '%smonthsago' % self.numago
        if self.date_type == 'year':
            return ''

    def get_crime_item(self):
        """ Return a Parse report.
            """
        parse = Parse('_input/%s' % self.build_filename())
        parse.set_crime(self.crime)
        parse.set_grep(self.grep)
        parse.set_location(self.location)
        # *** other types of reports
        result = parse.get_rankings()
        print result

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    """
    # Kill command-line usage for now
    parser = OptionParser()
    parser.add_option("-d", "--date_type", dest="date_type")
    parser.add_option("-n", "--numago", dest="numago")
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-o", "--output", dest="output", default="json")
    parser.add_option("-g", "--grep", dest="grep", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()


    report = Report(options.date_type, options.location, options.numago, options.output)
    report.get_crime_item()
    """
