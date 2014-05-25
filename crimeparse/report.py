#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (month / quarter / year) report. A higher-level interface to parse.py
#
# Takes input (report date type, crime, location) and returns report in output type desired (json, text)
from optparse import OptionParser
from parse import Parse
from datetime import datetime, timedelta

class Report:
    """ class Report is an interface with class Parse to pull out defined 
        crime queries ( crime_items ). Report takes a dict of crime_item definitions:
        { 
            'slug': '[[slug]]', 'name': '[[full-name]]', 
            'date_type': 'month', 'numago': '0', 'report_type': 'rankings',
            'location': 'capitol-hill', 'crime': 'violent', 'grep': False 
        }
        """

    def __init__(self, *args, **kwargs):
        self.set_date_type(None)
        self.set_location(None)
        self.set_numago(None)
        self.set_report_type('rankings')
        for key, value in kwargs.iteritems():
            if key == 'date_type':
                self.set_date_type(value)
            elif key == 'location' and value != '':
                self.set_location(value)
            elif key == 'output':
                self.set_output(value)
            elif key == 'crime':
                self.set_crime(value)
            elif key == 'grep':
                self.set_grep(value)
            elif key == 'numago':
                self.set_numago(value)
            elif key == 'report_type':
                self.set_report_type(value)

        # This comes last because we need to know what self.numago is to run this.
        if args and args[0] != '':
            self.set_timespan(args, self.numago)

    def set_timespan(self, value, numago=0):
        """ Set the object's timespan var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> timespan = report.set_timespan(['2013-01-08', '2013-11-27'])
            >>> print timespan
            [datetime.datetime(2013, 1, 8, 0, 0), datetime.datetime(2013, 11, 27, 0, 0)]
            """
        time_from = datetime.strptime(value[0], '%Y-%m-%d')
        time_to = datetime.strptime(value[1], '%Y-%m-%d')
        if numago > 0:
            delta = 1 + (numago * 365)
            time_from = time_from - timedelta(delta)
            time_to = time_to - timedelta(delta)

        self.timespan = [time_from, time_to]
        return self.timespan

    def set_report_type(self, value):
        """ Set the object's report_type var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> report_type = report.set_report_type('specific')
            >>> print report_type
            specific
            """
        self.report_type = value
        return self.report_type

    def set_date_type(self, value):
        """ Set the object's date_type var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> date_type = report.set_date_type('quarter')
            >>> print date_type
            quarter
            """
        self.date_type = value
        return self.date_type

    def set_numago(self, value):
        """ Set the object's numago var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> numago = report.set_numago(1)
            >>> print numago
            1
            """
        self.numago = value
        return self.numago

    def set_crime(self, value):
        """ Set the object's crime var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> crime = report.set_crime('property')
            >>> print crime
            property
            """
        self.crime = value
        return self.crime

    def set_grep(self, value):
        """ Set the object's grep var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> grep = report.set_grep('True')
            >>> print grep
            True
            """
        self.grep = value
        if value == 'True':
            self.grep = True
        elif value == 'False':
            self.grep = False
        return self.grep

    def set_location(self, value):
        """ Set the object's location var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> location = report.set_location('cbd')
            >>> print location
            cbd
            """
        self.location = value
        return self.location

    def set_output(self, value):
        """ Set the object's output var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> output = report.set_output('text')
            >>> print output
            text
            """
        self.output = value
        return self.output

    def build_filename(self):
        """ Put together the pieces we need to get the filename we query.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> filename = report.build_filename()
            >>> print filename
            1monthsago
            """
        if self.numago == None:
            self.set_numago(0)

        if self.date_type == 'test':
            return 'test'
        if self.date_type == 'month':
            # We would never query the current month, it's never complete.
            # That's why we offset all month-queries by one.
            self.set_numago(self.numago + 1)
            return '%smonthsago' % self.numago
        if self.date_type == 'year':
            return datetime.now().year - self.numago

    def get_crime_item(self):
        """ Return a Parse report.
            """
        parse = Parse('_input/%s' % self.build_filename())
        parse.set_crime(self.crime)
        parse.set_grep(self.grep)
        parse.set_location(self.location)
        # *** Can't uncomment this until we merge with master
        #if self.timespan:
        #    parse.set_timespan(self.timespan)
        # *** other types of reports
        if self.report_type == 'rankings':
            result = parse.get_rankings()
        elif self.report_type == 'specific':
            result = parse.get_specific_crime()
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
