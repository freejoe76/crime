#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a year-over-year report.
from report import Report
from optparse import OptionParser

report_items = [ 
        { 'slug': 'violent', 'name': 'Violent', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'violent', 'grep': False  },
        #{ 'slug': 'property', 'name': 'Property', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'property', 'grep': False },
]

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="year")
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()

    for item in report_items:
        item['date_type'] = options.date_type
        item['location'] = options.location
        for yearback in [0, 1, 2, 3]:
            item['numago'] = yearback
            report = Report(*args, **item)
            print report.get_crime_item()
