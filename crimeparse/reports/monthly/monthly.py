#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a monthly report.
from report import Report
from optparse import OptionParser

report_items = { 
        { 'slug': 'violent', 'name': 'Violent',  'date_type': 'month', 'location': '', 'crime': 'violent', 'grep': False },
        { 'slug': 'dv', 'name': 'Domestic Violence',  'date_type': 'month', 'location': '', 'crime': 'dv', 'grep': True },
        { 'slug': 'property', 'name': 'Property',  'date_type': 'month', 'location': '', 'crime': 'property', 'grep': False },
        { 'slug': 'robbery', 'name': 'Robbery',  'date_type': 'month', 'location': '', 'crime': 'robbery', 'grep': True },
        { 'slug': 'burgle', 'name': 'Burglary',  'date_type': 'month', 'location': '', 'crime': 'burg', 'grep': True },
        { 'slug': 'burgle_residence', 'name': 'Burglary: Residential',  'date_type': 'month', 'location': '', 'crime': 'burglary-residence', 'grep': True },
        { 'slug': 'burgle_business', 'name': 'Burglary: Business',  'date_type': 'month', 'location': '', 'crime': 'burglary-business', 'grep': True },
        { 'slug': 'burgle_forced', 'name': 'Burglary: Forced',  'date_type': 'month', 'location': '', 'crime': 'by-force', 'grep': True },
        { 'slug': 'burgle_unforced', 'name': 'Burglary: Unforced',  'date_type': 'month', 'location': '', 'crime': 'no-force', 'grep': True },
        { 'slug': 'theft_car', 'name': 'Car Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-of-motor-vehicle', 'grep': False },
        { 'slug': 'theft_bike', 'name': 'Bike Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-bicycle', 'grep': False }
}

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()

    for item in report_items:
        if options.location != None:
            item['location'] = options.location
        print item
        report = Report(**item)
        report.get_crime_item()

