#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a month-over-month report.
# Pass it a date param -- months are defined as 30 days, the month will 
# end on the date passed and then work its way back.
# Usage:
# $ cd crime/crimeparse; python -m reports.monthly.monthover 2016-01-30
from report import Report
from optparse import OptionParser
from datetime import date

report_items = [ 
        #{ 'slug': 'assault', 'name': 'Assault', 'date_type': 'month', 'location': '', 'crime': 'assault', 'grep': True },
        { 'slug': 'violent', 'name': 'Violent',  'date_type': 'month', 'location': '', 'crime': 'violent', 'grep': False },
        #{ 'slug': 'homicide', 'name': 'Homicide', 'date_type': 'month', 'location': '', 'crime': 'murder', 'grep': False  },
]
"""
        { 'slug': 'rape', 'name': 'Rape', 'date_type': 'month', 'location': '', 'crime': 'sex-aslt-rape', 'grep': False  },
        { 'slug': 'property', 'name': 'Property',  'date_type': 'month', 'location': '', 'crime': 'property', 'grep': False },
        { 'slug': 'dv', 'name': 'Domestic Violence',  'date_type': 'month', 'location': '', 'crime': 'dv', 'grep': True },
        { 'slug': 'robbery', 'name': 'Robbery',  'date_type': 'month', 'location': '', 'crime': 'robbery', 'grep': True },
        { 'slug': 'theft_car', 'name': 'Car Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-of-motor-vehicle', 'grep': False },
        { 'slug': 'theft_bike', 'name': 'Bike Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-bicycle', 'grep': False },
        { 'slug': 'burglary-forced', 'name': 'Burglary: Forced',  'date_type': 'monthly', 'location': '', 'crime': 'by-force', 'grep': True },
        { 'slug': 'burglary-unforced', 'name': 'Burglary: Unforced',  'date_type': 'monthly', 'location': '', 'crime': 'no-force', 'grep': True },
        { 'slug': 'burglary-business-forced', 'name': 'Burglary: Business: Forced',  'date_type': 'monthly', 'location': '', 'crime': 'burglary-business-by-force', 'grep': True},
        { 'slug': 'burglary-business-unforced', 'name': 'Burglary: Business: Unforced',  'date_type': 'monthly', 'location': '', 'crime': 'burglary-business-no-force', 'grep': True},
        { 'slug': 'burglary-business', 'name': 'Burglary: Business',  'date_type': 'monthly', 'location': '', 'crime': 'burglary-business', 'grep': True},
        { 'slug': 'burglary-residence-forced', 'name': 'Burglary: Residence: Forced',  'date_type': 'monthly', 'location': '', 'crime': 'burglary-residence-by-force', 'grep': True},
        { 'slug': 'burglary-residence-unforced', 'name': 'Burglary: Residence: Unforced',  'date_type': 'monthly', 'location': '', 'crime': 'burglary-residence-no-force', 'grep': True},
        { 'slug': 'burglary-residence', 'name': 'Burglary: Residence',  'date_type': 'monthly', 'location': '', 'crime': 'burglary-residence', 'grep': True},
]
"""

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="month")
    parser.add_option("-r", "--report", dest="report_type", default="rankings")
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
    (options, args) = parser.parse_args()

    for item in report_items:
        if options.verbose == True:
            print item['name']
        item['date_type'] = options.date_type
        item['location'] = options.location
        item['report_type'] = options.report_type

        for ago in [0, 1, 2]:
            item['numago'] = ago 
            report = Report(*args, **item)
            if item['report_type'] == 'rankings':
                print '"%s__%d": ' % ( item['slug'], ago ) 
                print report.get_crime_item(),
                print ","
            else:
                print report.get_crime_item()
