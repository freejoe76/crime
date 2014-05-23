#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a year-over-year report.
from report import Report
from optparse import OptionParser

report_items = { 
        'violent': { 'name': 'Violent', 'options': { 'date_type': '', 'location': '', 'crime': 'violent', 'grep': False } },
        'property': { 'name': 'Property', 'options': { 'date_type': '', 'location': '', 'crime': 'property', 'grep': False } },
}

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="year")
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()

    for item in report_items:
        report_items[item]['options']['type'] = options.date_type
        if options.location != None:
            report_items[item]['options']['location'] = options.location
        print report_items[item]
        for yearback in [0, 1, 2, 3]:
            report_items[item]['options']['numago'] = yearback
            report = Report(**{item: report_items[item]})
            report.get_crime_item()
