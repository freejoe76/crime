#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a monthly report.
from report import Report
from optparse import OptionParser

report_items = { 
        'violent': { 'name': 'Violent', 'options': { 'type': 'month', 'location': '', 'crime': 'violent', 'grep': False } },
        'dv': { 'name': 'Domestic Violence', 'options': { 'type': 'month', 'location': '', 'crime': 'dv', 'grep': True} },
        'property': { 'name': 'Property', 'options': { 'type': 'month', 'location': '', 'crime': 'property', 'grep': False} },
        'robbery': { 'name': 'Robbery', 'options': { 'type': 'month', 'location': '', 'crime': 'robbery', 'grep': True} },
        'burgle': { 'name': 'Burglary', 'options': { 'type': 'month', 'location': '', 'crime': 'burg', 'grep': True} },
        'burgle_residence': { 'name': 'Burglary: Residential', 'options': { 'type': 'month', 'location': '', 'crime': 'burglary-residence', 'grep': True} },
        'burgle_business': { 'name': 'Burglary: Business', 'options': { 'type': 'month', 'location': '', 'crime': 'burglary-business', 'grep': True} },
        'burgle_forced': { 'name': 'Burglary: Forced', 'options': { 'type': 'month', 'location': '', 'crime': 'by-force', 'grep': True} },
        'burgle_unforced': { 'name': 'Burglary: Unforced', 'options': { 'type': 'month', 'location': '', 'crime': 'no-force', 'grep': True} },
        'theft_car': { 'name': 'Car Theft', 'options': { 'type': 'month', 'location': '', 'crime': 'theft-of-motor-vehicle', 'grep': False} },
        'theft_bike': { 'name': 'Bike Theft', 'options': { 'type': 'month', 'location': '', 'crime': 'theft-bicycle', 'grep': False} }
}

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()

    for item in report_items:
        if options.location != None:
            report_items[item]['options']['location'] = options.location
        print report_items[item]
        report = Report(**{item: report_items[item]})
        report.get_crime_item()

