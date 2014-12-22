#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a monthly report.
# Usage:
# $ cd crime/crimeparse; python -m reports.monthly.monthly
from report import Report
from optparse import OptionParser
from datetime import date

report_items = [ 
        { 'slug': 'assault', 'name': 'Assault', 'date_type': 'month', 'location': '', 'crime': 'assault', 'grep': True },
        { 'slug': 'homicide', 'name': 'Homicide', 'date_type': 'month', 'location': '', 'crime': 'murder', 'grep': False  },
        { 'slug': 'rape', 'name': 'Rape', 'date_type': 'month', 'location': '', 'crime': 'sex-aslt-rape', 'grep': False  },
        { 'slug': 'violent', 'name': 'Violent',  'date_type': 'month', 'location': '', 'crime': 'violent', 'grep': False },
        { 'slug': 'property', 'name': 'Property',  'date_type': 'month', 'location': '', 'crime': 'property', 'grep': False },
        { 'slug': 'dv', 'name': 'Domestic Violence',  'date_type': 'month', 'location': '', 'crime': 'dv', 'grep': True },
        { 'slug': 'robbery', 'name': 'Robbery',  'date_type': 'month', 'location': '', 'crime': 'robbery', 'grep': True },
        { 'slug': 'burgle', 'name': 'Burglary',  'date_type': 'month', 'location': '', 'crime': 'burg', 'grep': True },
        { 'slug': 'burgle_residence', 'name': 'Burglary: Residential',  'date_type': 'month', 'location': '', 'crime': 'burglary-residence', 'grep': True },
        { 'slug': 'burgle_business', 'name': 'Burglary: Business',  'date_type': 'month', 'location': '', 'crime': 'burglary-business', 'grep': True },
        { 'slug': 'burgle_forced', 'name': 'Burglary: Forced',  'date_type': 'month', 'location': '', 'crime': 'by-force', 'grep': True },
        { 'slug': 'burgle_unforced', 'name': 'Burglary: Unforced',  'date_type': 'month', 'location': '', 'crime': 'no-force', 'grep': True },
        { 'slug': 'theft_car', 'name': 'Car Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-of-motor-vehicle', 'grep': False },
        { 'slug': 'theft_bike', 'name': 'Bike Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-bicycle', 'grep': False }
]

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="month")
    parser.add_option("-r", "--report", dest="report_type", default="specific")
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
    (options, args) = parser.parse_args()

    for item in report_items:
        if options.verbose == True:
            print item['name']
        item['date_type'] = options.date_type
        item['location'] = options.location
        item['report_type'] = options.report_type
        year = date.today().year
        for yearback in [0, 1, 2, 3, 4, 5, 6]:
            item['numago'] = yearback
            report = Report(*args, **item)
            # Rankings output comes default in specific report,
            # so if we're specifying rankings as the report_type that means
            # we're using this output for something else... something else that
            # needs it in ready-to-write-the-compiled-json-to-a-file format.
            if item['report_type'] == 'rankings':
                print '"%s__%d": ' % ( item['slug'], year - yearback ) 
                print report.get_crime_item(),
                print ","
            else:
                print report.get_crime_item()
