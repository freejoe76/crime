#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a monthly report on crime in a particular month.
# Usage:
# $ cd crime/crimeparse; python -m reports.monthly.monthly
from report import Report
from optparse import OptionParser
from datetime import date
import json

report_items = [ 
        { 'slug': 'assault', 'name': 'Assault', 'date_type': 'month', 'location': '', 'crime': 'assault', 'grep': True },
        { 'slug': 'homicide', 'name': 'Homicide', 'date_type': 'month', 'location': '', 'crime': 'murder', 'grep': False },
        { 'slug': 'rape', 'name': 'Rape', 'date_type': 'month', 'location': '', 'crime': 'sex-aslt-rape', 'grep': False },
        { 'slug': 'violent', 'name': 'Violent',  'date_type': 'month', 'location': '', 'crime': 'violent', 'grep': False },
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
        { 'slug': 'drug-alcohol', 'name': 'Drug and Alcohol',  'date_type': 'monthly', 'location': '', 'crime': 'drug-alcohol', 'grep': False},
        { 'slug': 'drug', 'name': 'Drug',  'date_type': 'monthly', 'location': '', 'crime': 'drug', 'grep': True},
        #{ 'slug': 'drug-poss', 'name': 'Drug: Paraphernalia Possesion',  'date_type': 'monthly', 'location': '', 'crime': 'drug-poss', 'grep': True},
        #{ 'slug': 'drug-synth', 'name': 'Drug: synth',  'date_type': 'monthly', 'location': '', 'crime': 'drug-synth', 'grep': True},
        #{ 'slug': 'drug-opium', 'name': 'Drug: opium',  'date_type': 'monthly', 'location': '', 'crime': 'drug-opium', 'grep': True},
        #{ 'slug': 'drug-marijuana', 'name': 'Drug: Marijuana',  'date_type': 'monthly', 'location': '', 'crime': 'drug-mari', 'grep': True},
        #{ 'slug': 'drug-heroin', 'name': 'Drug: heroin',  'date_type': 'monthly', 'location': '', 'crime': 'drug-heroin', 'grep': True},
        #{ 'slug': 'drug-cocaine', 'name': 'Drug: cocaine',  'date_type': 'monthly', 'location': '', 'crime': 'drug-cocaine', 'grep': True},
        #{ 'slug': 'drug-pcs', 'name': 'Drug: pcs / other',  'date_type': 'monthly', 'location': '', 'crime': 'drug-pcs', 'grep': True},
        #{ 'slug': 'drug-meth', 'name': 'Drug: Meth',  'date_type': 'monthly', 'location': '', 'crime': 'drug-meth', 'grep': True},
        #{ 'slug': 'drug-hallu', 'name': 'Drug: Hallucinogen',  'date_type': 'monthly', 'location': '', 'crime': 'drug-hallu', 'grep': True},
]

def yearmonth_subtract(ym):
    """ Given a yearmonth, ala 201604, return the next-lower month.
        """
    ym = int(ym)
    if ym % 100 == 1:
        # We return the previous year
        return ym - 89
    return ym - 1

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="monthly")
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
        year = date.today().year
        month = date.today().month
        ym = '%d%d' % (year, month)
        if month < 10:
            ym = '%d0%d' % (year, month)

        for ago in range(24):
            item['numago'] = ago 
            report = Report(*args, **item)
            report.set_timespan('', ago)
            # Rankings output comes default in specific report,
            # so if we're specifying rankings as the report_type that means
            # we're using this output for something else... something else that
            # needs it in ready-to-write-the-compiled-json-to-a-file format.
            if item['report_type'] == 'rankings':
                print '"%s__%d": ' % ( item['slug'], int(ym) ) 
                print '%s,' % json.dumps(report.get_crime_item()),
            else:
                print report.get_crime_item()
            ym = yearmonth_subtract(ym)
