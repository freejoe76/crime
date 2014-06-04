#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a year-over-year report.
from report import Report
from optparse import OptionParser

report_items = [ 
        { 'slug': 'violent', 'name': 'Violent', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'violent', 'grep': False  },
]
"""
        { 'slug': 'drug-sell', 'name': 'Drug: Selling', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug*sell', 'grep': True},
        { 'slug': 'drug-possess', 'name': 'Drug: Possession', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug*possess', 'grep': True},
        { 'slug': 'car-theft', 'name': 'Car Thefts', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'theft-of-motor-vehicle', 'grep': False  },
        { 'slug': 'bike-theft', 'name': 'Bike Thefts', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'theft-bicycle', 'grep': False  },
        { 'slug': 'burglary-business', 'name': 'Burglary: Business', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'burglary-business', 'grep': True},
        { 'slug': 'burglary-residence', 'name': 'Burglary: Residence', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'burglary-residence', 'grep': True},
        { 'slug': 'property', 'name': 'Property', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'property', 'grep': False },
        { 'slug': 'drug-alcohol', 'name': 'Drug and Alcohol', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-alcohol', 'grep': False},
        { 'slug': 'drug-poss', 'name': 'Drug: Paraphernalia Possesion', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-poss', 'grep': True},
        { 'slug': 'drug-synth', 'name': 'Drug: synth', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-synth', 'grep': True},
        { 'slug': 'drug-opium', 'name': 'Drug: opium', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-opium', 'grep': True},
        { 'slug': 'drug', 'name': 'Drug', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug', 'grep': True},
        { 'slug': 'drug-marijuana', 'name': 'Drug: Marijuana', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-mari', 'grep': True},
        { 'slug': 'drug-heroin', 'name': 'Drug: heroin', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-heroin', 'grep': True},
        { 'slug': 'drug-cocaine', 'name': 'Drug: cocaine', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-cocaine', 'grep': True},
        { 'slug': 'drug-pcs', 'name': 'Drug: pcs / other', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-pcs', 'grep': True},
        { 'slug': 'drug-meth', 'name': 'Drug: Meth', 'report_type': 'specific', 'date_type': '', 'location': '', 'crime': 'drug-meth', 'grep': True},
"""

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="year")
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=True)
    (options, args) = parser.parse_args()

    for item in report_items:
        print item
        item['date_type'] = options.date_type
        item['location'] = options.location
        for yearback in [0, 1, 2, 3]:
            item['numago'] = yearback
            report = Report(*args, **item)
            print report.get_crime_item()
