#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (month / year) report. A higher-level interface to parse.py
#
# Takes input (report date type, crime, location) and returns report in json
# Example command (assumes report config file in ./reports/yoy/yoy.py ):
# $ python -m reports.yoy.yoy 2014-01-01 2014-07-31 --location capitol-hill
from optparse import OptionParser
from parse import Parse
from datetime import datetime, date, timedelta

class Report:
    """ class Report is an interface with class Parse to pull out defined 
        crime queries ( crime_items ). Report takes a dict of crime_item definitions:
        { 
            'slug': '[[slug]]', 'name': '[[full-name]]', 
            'date_type': 'monthly', 'numago': '0', 'report_type': 'rankings',
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

    def last_day_of_a_month(self, d):
        """ Return a date object of the last day of the month of the dat object
            provided.
            >>> report = Report(**{'date_type': 'monthly', 'location': 'capitol-hill'})
            >>> d = date(2016, 8, 3)
            >>> print report.last_day_of_a_month(d)
            date(2016, 8, 31)
            """
        next_month = d.replace(day=28) + timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def set_timespan(self, value, numago=0):
        """ Set the object's timespan var.
            numago defines the number of years previous to the initial timestamp.
            >>> report = Report(**{'date_type': 'monthly', 'location': 'capitol-hill'})
            >>> timespan = report.set_timespan(['2013-01-08', '2013-11-27'])
            >>> print timespan
            [datetime.date(2013, 1, 8), datetime.date(2013, 11, 27)]
            """
        if self.date_type == 'month':
            # Monthly is for specific months. Start with current month
            # and go from there.
            d = date.today()
            time_from = d.replace(day=1)
            time_to = self.last_day_of_a_month(time_from)
        elif self.date_type == 'monthly':
            # Monthly only takes one value: The date you want to start counting
            # backward to figure out the month from.
            # We're defining "month" here as "any 30 day period of time."
            time_to = datetime.strptime(value[0], '%Y-%m-%d').date()
            time_from = time_to - timedelta(30)
        else:
            time_from = datetime.strptime(value[0], '%Y-%m-%d').date()
            time_to = datetime.strptime(value[1], '%Y-%m-%d').date()

        if numago > 0:
            if self.date_type == 'month':
                # Calculate a previous month, based on numago, which is how
                # many months back we go.
                months = numago % 12
                if months >= time_from.month:
                    time_from = time_from.replace(year=time_from.year - 1)
                    time_from = time_from.replace(month=12-(months - time_from.months))
                else:
                    time_from = time_from.replace(month=(time_from.months - months))
                if numago - months > 0:
                    years = int((numago-months)/12)
                    time_from = time_from.replace(year=time_from.year - years)
                time_to = self.last_day_of_a_month(time_from)
            elif self.date_type == 'monthly':
                daysago = numago * 30
                # The +1 makes sure that we're not counting the crimes on the
                # border dates twice.
                # If our first date range was January 1-31, we want the next
                # one to be December 1-31, not December 2-Jan 1.
                time_from = time_from - timedelta(daysago + 1)
                time_to = time_to - timedelta(daysago + 1)
            else:
                time_from = date(time_from.year - numago, time_from.month, time_from.day)
                try:
                    time_to = date(time_to.year - numago, time_to.month, time_to.day)
                except ValueError as e:
                    if e == 'day is out of range for month':
                        time_to = date(time_to.year - numago, time_to.month, time_to.day - 1)
                    else:
                        raise ValueError

        self.timespan = [time_from, time_to]
        return self.timespan

    def set_report_type(self, value):
        """ Set the object's report_type var.
            >>> report = Report(**{'date_type': 'monthly', 'location': 'capitol-hill'})
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
            >>> report = Report(**{'date_type': 'monthly', 'location': 'capitol-hill'})
            >>> filename = report.build_filename()
            >>> print filename
            last4months
            """
        if self.numago == None:
            self.numago = 0

        if self.date_type == 'test':
            return 'test'
        elif self.date_type == 'month':
            return 'last12months'
            return 'current'
        elif self.date_type == 'monthly':
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
