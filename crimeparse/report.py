#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (month / year) report. A higher-level interface to parse.py
#
# Takes input (report date type, crime, location) and returns report in json
# Example command (assumes report config file in ./reports/yoy/yoy.py:
# $ python -m reports.yoy.yoy 2014-01-01 2014-07-31 --location capitol-hill
from optparse import OptionParser
from parse import Parse
from datetime import datetime, date, timedelta

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
        """ Set what we need to start a Report object.
            >>> r = Report()
            """
        self.grep = False
        self.set_report_type('rankings')
        for key, value in kwargs.iteritems():
            if key == 'date_type':
                self.date_type = value
            elif key == 'location' and value != '':
                self.location = value
            elif key == 'output':
                self.output = value
            elif key == 'crime':
                self.crime = value
            elif key == 'grep':
                self.grep = value
            elif key == 'numago':
                self.numago = value
            elif key == 'report_type':
                self.set_report_type(value)

        # This comes last because we need to know what self.numago is to run this.
        if args and args[0] != '':
            self.set_timespan(args, self.numago)

    def set_timespan(self, value, numago=0):
        """ Set the object's timespan var.
            numago defines the number of years previous to the initial timestamp.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> timespan = report.set_timespan(['2013-01-08', '2013-11-27'])
            >>> print timespan
            [datetime.date(2013, 1, 8), datetime.date(2013, 11, 27)]
            """
        if self.date_type == 'month':
            # Months only take one value: The date you want to start counting
            # backward to figure out the month from.
            # We're defining "month" here as "any 30 day period of time."
            time_to = datetime.strptime(value[0], '%Y-%m-%d').date()
            time_from = time_to - timedelta(30)
        else:
            time_from = datetime.strptime(value[0], '%Y-%m-%d').date()
            time_to = datetime.strptime(value[1], '%Y-%m-%d').date()

        if numago > 0:
            if self.date_type == 'month':
                daysago = numago * 30
                # The +1 makes sure that we're not counting the crimes on the
                # border dates twice.
                # If our first date range was January 1-31, we want the next
                # one to be December 1-31, not December 2-Jan 1.
                time_from = time_from - timedelta(daysago + 1)
                time_to = time_to - timedelta(daysago + 1)
            else:
                time_from = date(time_from.year - numago, time_from.month, time_from.day)
                time_to = date(time_to.year - numago, time_to.month, time_to.day)

        self.timespan = [time_from, time_to]
        return self.timespan

    def set_report_type(self, value):
        """ Set the object's report_type var.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> report_type = report.set_report_type('specific')
            >>> print report_type
            specific
            """
        approved_values = ['specific', 'rankings', 'recent', 'monthly', 'search', 'by-address']
        if value not in approved_values:
            raise ValueError('Report Type provided is not available.\nAvailable report types: %s' % approved_values)
        self.report_type = value
        return self.report_type

    def build_filename(self):
        """ Put together the pieces we need to get the filename we query.
            >>> report = Report(**{'date_type': 'month', 'location': 'capitol-hill'})
            >>> filename = report.build_filename()
            >>> print filename
            last4months
            """
        if self.numago == None:
            self.numago = 0

        if self.date_type == 'test':
            return 'test'
        elif self.date_type == 'month':
            # We would never query the current month, it's never complete.
            # That's why we offset all month-queries by one.
            self.numago += 4
            #return 'last12months'
            return 'last%smonths' % self.numago
        elif self.date_type == 'year':
            return 'current'
            #return datetime.now().year - self.numago
        return False

    def get_crime_item(self):
        """ Return a Parse report.
            >>> report = Report(**{'date_type': 'test', 'location': 'capitol-hill', 'report_type': 'specific'})
            >>> output = report.get_crime_item()
            >>> print output['count'], output['crime']
            29 None
            """
        fn = self.build_filename()
        parse = Parse('_input/%s' % fn)
        parse.crime = self.crime
        parse.grep = self.grep
        try:
            parse.location = self.location
        except:
            pass
        try:
            parse.set_timespan(self.timespan)
        except:
            pass

        # *** eventually we might want to allow for other types of reports
        if self.report_type == 'rankings':
            result = parse.get_rankings()
        elif self.report_type == 'specific':
            result = parse.get_specific_crime()
        return result

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
