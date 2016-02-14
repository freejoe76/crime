#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Config file for running a month-over-month report.
# Pass it a date param -- months are defined as 30 days, the month will 
# end on the date passed and then work its way back.
# Usage:
# $ cd crime/crimeparse; python -m reports.monthly.monthover 2016-01-30 --location capitol-hill
# Note: We need location parameter passed because that triggers the sorting and the ranking... for some reason.
from report import Report
from collections import OrderedDict
import operator
from optparse import OptionParser
from datetime import date

report_items = [ 
        { 'slug': 'traffic-accident-hit-and-run', 'name': 'Hit and Runs',  'date_type': 'month', 'location': '', 'crime': 'traffic-accident-hit-and-run', 'grep': False },
        { 'slug': 'traffic-accident-dui-duid', 'name': 'DUI',  'date_type': 'month', 'location': '', 'crime': 'traffic-accident-dui-duid', 'grep': False },
        { 'slug': 'aggravated-assault', 'name': 'Serious Assault',  'date_type': 'month', 'location': '', 'crime': 'aggravated-assault' },
        { 'slug': 'assault', 'name': 'All Assaults', 'date_type': 'month', 'location': '', 'crime': 'assault', 'grep': True },
        { 'slug': 'homicide', 'name': 'Homicide', 'date_type': 'month', 'location': '', 'crime': 'murder', 'grep': False  },
        { 'slug': 'violent', 'name': 'Violent',  'date_type': 'month', 'location': '', 'crime': 'violent', 'grep': False },
        { 'slug': 'rape', 'name': 'Rape', 'date_type': 'month', 'location': '', 'crime': 'sex-aslt-rape', 'grep': False  },
        { 'slug': 'property', 'name': 'Property',  'date_type': 'month', 'location': '', 'crime': 'property', 'grep': False },
        { 'slug': 'dv', 'name': 'Domestic Violence',  'date_type': 'month', 'location': '', 'crime': 'dv', 'grep': True },
        { 'slug': 'sexual-assault', 'name': 'Sexual Assault',  'date_type': 'month', 'location': '', 'crime': 'sexual-assault', 'grep': False },
        { 'slug': 'robbery', 'name': 'Robbery',  'date_type': 'month', 'location': '', 'crime': 'robbery', 'grep': True },
        { 'slug': 'robbery-bank', 'name': 'Bank Robbery',  'date_type': 'month', 'location': '', 'crime': 'robbery-bank', 'grep': False },
        { 'slug': 'robbery-car-jacking', 'name': 'Carjacking',  'date_type': 'month', 'location': '', 'crime': 'robbery-car-jacking', 'grep': False },
        { 'slug': 'auto-theft', 'name': 'Car Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-of-motor-vehicle', 'grep': False },
        { 'slug': 'theft_bicycle', 'name': 'Bike Theft',  'date_type': 'month', 'location': '', 'crime': 'theft-bicycle', 'grep': False },
        { 'slug': 'by-force', 'name': 'Burglary: Forced',  'date_type': 'month', 'location': '', 'crime': 'by-force', 'grep': True },
        { 'slug': 'no-force', 'name': 'Burglary: Unforced',  'date_type': 'month', 'location': '', 'crime': 'no-force', 'grep': True },
        { 'slug': 'burglary-business-by-force', 'name': 'Burglary: Business: Forced',  'date_type': 'month', 'location': '', 'crime': 'burglary-business-by-force', 'grep': True},
        { 'slug': 'burglary-business-no-force', 'name': 'Burglary: Business: Unforced',  'date_type': 'month', 'location': '', 'crime': 'burglary-business-no-force', 'grep': True},
        { 'slug': 'burglary-business', 'name': 'Burglary: Business',  'date_type': 'month', 'location': '', 'crime': 'burglary-business', 'grep': True},
        { 'slug': 'burglary-residence-by-force', 'name': 'Burglary: Residence: Forced',  'date_type': 'month', 'location': '', 'crime': 'burglary-residence-by-force', 'grep': True},
        { 'slug': 'burglary-residence-no-force', 'name': 'Burglary: Residence: Unforced',  'date_type': 'month', 'location': '', 'crime': 'burglary-residence-no-force', 'grep': True},
        { 'slug': 'burglary-residence', 'name': 'Burglary: Residence',  'date_type': 'month', 'location': '', 'crime': 'burglary-residence', 'grep': True},
        { 'slug': 'prostitution', 'name': 'Prostitution',  'date_type': 'month', 'location': '', 'crime': 'prostitution', 'grep': True },
        { 'slug': 'public-fighting', 'name': 'Public Fighting',  'date_type': 'month', 'location': '', 'crime': 'public-fighting', 'grep': False },
        { 'slug': 'arson', 'name': 'Arson',  'date_type': 'month', 'location': '', 'crime': 'arson', 'grep': False },
]

report_items = [ 
        { 'slug': 'traffic-accident-hit-and-run', 'name': 'Hit and Runs',  'date_type': 'month', 'location': '', 'crime': 'traffic-accident-hit-and-run', 'grep': False },
]

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

        comparison = []
        for ago in [0, 1, 2]:
            item['numago'] = ago 
            report = Report(*args, **item)
            if item['report_type'] == 'rankings':
                crime_item = report.get_crime_item(),
                comparison.append(crime_item)
                print '"%s__%d": ' % ( item['slug'], ago ) 
                print crime_item
                print ","
            else:
                print report.get_crime_item()

        print '========'
        risers = {'count': {}, 'rank': {}}
        fallers = {'count': {}, 'rank': {}}
        if len(comparison) > 0:
            # Loop through the stored crime items and generate a fastest-risers
            # and fastest-fallers report.
            # We need the rise/fall report for per-capita count and for ranking.
            for i in range(0, len(comparison) - 1):
                # Compare each item in the current set to the set that follows.
                # Make note of the difference in count and ranking.
                for record in comparison[i][0]['crimes']['percapita']:
                    print record, comparison[i][0]['crimes']['percapita'][record]
                    diff = round(comparison[i][0]['crimes']['percapita'][record]['count'] - comparison[i+1][0]['crimes']['percapita'][record]['count'], 3)
                    if diff != 0:
                        if diff > 0:
                            risers['count'][record] = diff
                        else:
                            fallers['count'][record] = diff
                    if comparison[i][0]['crimes']['percapita'][record]['count'] == 0:
                        continue
                    diff = comparison[i][0]['crimes']['percapita'][record]['rank'] - comparison[i+1][0]['crimes']['percapita'][record]['rank']
                    if diff > 0:
                        risers['rank'][record] = diff
                    else:
                        fallers['rank'][record] = diff
        risers['count'] = sorted(risers['count'].iteritems(), key=operator.itemgetter(1), reverse=True)
        risers['rank'] = sorted(risers['rank'].iteritems(), key=operator.itemgetter(1), reverse=True)
        fallers['count'] = sorted(fallers['count'].iteritems(), key=operator.itemgetter(1), reverse=True)
        fallers['rank'] = sorted(fallers['rank'].iteritems(), key=operator.itemgetter(1), reverse=True)
        print '"%s__%d__risers": ' % ( item['slug'], i) 
        print risers
        print ","
        print '"%s__%d__fallers": ' % ( item['slug'], i) 
        print fallers
        print ","
