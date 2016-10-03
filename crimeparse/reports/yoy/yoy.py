#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a year-over-year report.
from report import Report
from datetime import date
from optparse import OptionParser

report_items = [ 
        { 'slug': 'weapon-fire', 'name': 'Weapon Fired', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'weapon-fire', 'grep': True },
        { 'slug': 'traffic-accident-hit-and-run', 'name': 'Hit and Runs', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'traffic-accident-hit-and-run', 'grep': False },
        { 'slug': 'traffic-accident-dui-duid', 'name': 'DUI', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'traffic-accident-dui-duid', 'grep': False },
        { 'slug': 'assault', 'name': 'All Assaults', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'assault', 'grep': True },
        { 'slug': 'aggravated-assault', 'name': 'Serious Assault', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'aggravated-assault' },
        #{ 'slug': 'assault-simple', 'name': 'Minor Assault', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'assault-simple' },
        { 'slug': 'homicide', 'name': 'Homicide', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'murder', 'grep': False  },
        { 'slug': 'rape', 'name': 'Rape', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'sex-aslt-rape', 'grep': False  },
        { 'slug': 'violent', 'name': 'Violent', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'violent', 'grep': False  },
        { 'slug': 'property', 'name': 'Property', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'property', 'grep': False },
        { 'slug': 'dv', 'name': 'Domestic Violence',  'date_type': '', 'location': '', 'crime': 'dv', 'grep': True },
        { 'slug': 'sexual-assault', 'name': 'Sexual Assault',  'date_type': '', 'location': '', 'crime': 'sexual-assault', 'grep': False },
        { 'slug': 'robbery', 'name': 'Robbery',  'date_type': '', 'location': '', 'crime': 'robbery', 'grep': True },
        { 'slug': 'burglary', 'name': 'Burglary',  'date_type': '', 'location': '', 'crime': 'burglary', 'grep': False },
        { 'slug': 'robbery-bank', 'name': 'Bank Robbery',  'date_type': '', 'location': '', 'crime': 'robbery-bank', 'grep': False },
        { 'slug': 'robbery-car-jacking', 'name': 'Carjacking',  'date_type': '', 'location': '', 'crime': 'robbery-car-jacking', 'grep': False },
        { 'slug': 'prostitution', 'name': 'Prostitution',  'date_type': '', 'location': '', 'crime': 'prostitution', 'grep': True },
        { 'slug': 'public-fighting', 'name': 'Public Fighting',  'date_type': '', 'location': '', 'crime': 'public-fighting', 'grep': False },
        { 'slug': 'arson', 'name': 'Arson',  'date_type': '', 'location': '', 'crime': 'arson', 'grep': False },
        { 'slug': 'drug', 'name': 'Drug', 'report_type': '', '': '', 'location': '', 'crime': 'drug', 'grep': True},
        #{ 'slug': 'drug-sell', 'name': 'Drug: Selling', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug*sell', 'grep': True},
        #{ 'slug': 'drug-possess', 'name': 'Drug: Possession', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug*possess', 'grep': True},
        { 'slug': 'auto-theft', 'name': 'Car Thefts', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'auto-theft', 'grep': False  },
        { 'slug': 'theft-bicycle', 'name': 'Bike Thefts', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'theft-bicycle', 'grep': False  },
        { 'slug': 'by-force', 'name': 'Burglary: Forced',  'date_type': '', 'location': '', 'crime': 'by-force', 'grep': True },
        { 'slug': 'no-force', 'name': 'Burglary: Unforced',  'date_type': '', 'location': '', 'crime': 'no-force', 'grep': True },
        #{ 'slug': 'burglary-business-by-force', 'name': 'Burglary: Business: Forced', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'burglary-business-by-force', 'grep': True},
        #{ 'slug': 'burglary-business-no-force', 'name': 'Burglary: Business: Unforced', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'burglary-business-no-force', 'grep': True},
        { 'slug': 'burglary-business', 'name': 'Burglary: Business', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'burglary-business', 'grep': True},
        #{ 'slug': 'burglary-residence-by-force', 'name': 'Burglary: Residence: Forced', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'burglary-residence-by-force', 'grep': True},
        #{ 'slug': 'burglary-residence-no-force', 'name': 'Burglary: Residence: Unforced', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'burglary-residence-no-force', 'grep': True},
        { 'slug': 'burglary-residence', 'name': 'Burglary: Residence', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'burglary-residence', 'grep': True},
        ##{ 'slug': 'drug-alcohol', 'name': 'Drug and Alcohol', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-alcohol', 'grep': False},
        # { 'slug': 'drug-poss', 'name': 'Drug: Paraphernalia Possesion', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-poss', 'grep': True},
        # { 'slug': 'drug-synth', 'name': 'Drug: synth', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-synth', 'grep': True},
        # { 'slug': 'drug-opium', 'name': 'Drug: opium', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-opium', 'grep': True},
        { 'slug': 'marijuana', 'name': 'Drug: Marijuana', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'marijuana', 'grep': True},
        { 'slug': 'heroin', 'name': 'Drug: heroin', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'heroin', 'grep': True},
        ##{ 'slug': 'drug-cocaine', 'name': 'Drug: cocaine', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-cocaine', 'grep': True},
        # { 'slug': 'drug-pcs', 'name': 'Drug: pcs / other', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-pcs', 'grep': True},
        # { 'slug': 'drug-meth', 'name': 'Drug: Meth', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-meth', 'grep': True},
        # { 'slug': 'drug-hallu', 'name': 'Drug: Hallucinogen', 'report_type': '', 'date_type': '', 'location': '', 'crime': 'drug-hallu', 'grep': True},
]

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-d", "--date_type", dest="date_type", default="year")
    parser.add_option("-r", "--report", dest="report_type", default="specific")
    #parser.add_option("-c", "--crime", dest="crime", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
    (options, args) = parser.parse_args()

    today = date.today()

    for item in report_items:
        if options.verbose == True:
            print item['name']
            print args
        item['date_type'] = options.date_type
        item['location'] = options.location
        item['report_type'] = options.report_type
        year = today.year
        #for yearback in [0, 1, 2, 3]:
        for yearback in [0, 1]:
            item['numago'] = yearback
            report = Report(*args, **item)

            # Rankings output comes default in specific report,
            # so if we're specifying rankings as the report_type that means
            # we're using this output for something else... something else that
            # needs it in ready-to-write-the-compiled-json-to-a-file format.
            if item['report_type'] in ['rankings', 'specific']:
                if today.month == 1 and today.day < 21:
                    yearback += 1
                print '"%s__%d": ' % ( item['slug'], year - yearback ) 
                print report.get_crime_item(),
                print ","
            else:
                print report.get_crime_item()
