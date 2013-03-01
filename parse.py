#!/usr/bin/python
# Run a query against the crime CSV's
import os
import csv
import operator
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime, timedelta

crime_genres = ['violent', 'property', 'other']
crime_lookup_reverse = { 
    'violent': ['murder', 'robbery', 'aggrvated-assault', 'sexual-assault'],
    'property': ['arson', 'theft-from-motor-vehicle', 'auto-theft', 'burglary', 'larceny'],
    'other': ['all-other-crimes', 'drug-alcohol', 'other-crimes-against-persons', 'white-collar-crime', 'public-disorder'] }
crime_lookup = {
    'all-other-crimes': 'other',
    'murder': 'violent',
    'arson': 'property',
    'theft-from-motor-vehicle': 'property',
    'auto-theft': 'property',
    'sexual-assault': 'violent',
    'drug-alcohol': 'other',
    'larceny': 'property',
    'aggravated-assault': 'violent',
    'other-crimes-against-persons': 'other',
    'robbery': 'violent',
    'burglary': 'property',
    'white-collar-crime': 'other',
    'public-disorder': 'other'
}
crime_types = ['criminal-mischief-mtr-veh', 'burglary-residence-no-force', 'vehicular-eluding-no-chase', 'traf-other', 'aslt-agg-police-gun', 'weapon-unlawful-discharge-of', 'theft-other', 'forgery-other', 'drug-barbiturate-possess', 'robbery-car-jacking', 'forgery-poss-of-forged-inst', 'failure-to-appear', 'theft-stln-veh-const-eqpt', 'arson-vehicle', 'liquor-possession', 'robbery-bank', 'other-enviornment-animal-viol', 'sex-aslt-non-rape', 'police-false-information', 'pawn-broker-viol', 'drug-methampetamine-possess', 'criminal-mischief-graffiti', 'burglary-business-by-force', 'weapon-carrying-concealed', 'harassment-dv', 'forgery-counterfeit-of-obj', 'drug-opium-or-deriv-sell', 'aggravated-assault', 'drug-cocaine-possess', 'robbery-street', 'theft-unauth-use-of-ftd', 'sex-off-fail-to-register', 'weapon-other-viol', 'violation-of-custody-order', 'theft-parts-from-vehicle', 'window-peeping', 'escape', 'violation-of-court-order', 'harassment', 'drug-fraud-to-obtain', 'criminal-mischief-other', 'theft-pick-pocket', 'bomb-threat', 'drug-hallucinogen-sell', 'aggravated-assault-dv', 'burglary-safe', 'arson-other', 'drug-poss-paraphernalia', 'theft-fail-return-rent-veh', 'theft-gas-drive-off', 'weapon-carrying-prohibited', 'weapon-by-prev-offender-powpo', 'theft-from-bldg', 'criminal-trespassing', 'liquor-misrepresent-age-minor', 'police-disobey-lawful-order', 'fraud-by-use-of-computer', 'burg-auto-theft-resd-w-force', 'drug-pcs-other-drug', 'drug-methampetamine-sell', 'burg-auto-theft-busn-w-force', 'impersonation-of-police', 'drug-marijuana-possess', 'theft-shoplift', 'assault-dv', 'fraud-identity-theft', 'theft-purse-snatch-no-force', 'drug-forgery-to-obtain', 'kidnap-dv', 'false-imprisonment', 'illegal-dumping', 'disturbing-the-peace', 'burg-auto-theft-resd-no-force', 'obstructing-govt-operation', 'public-fighting', 'police-making-a-false-rpt', 'weapon-poss-illegal-dangerous', 'indecent-exposure', 'harassment-sexual-in-nature', 'threats-to-injure', 'fireworks-possession', 'vehicular-eluding', 'drug-methamphetamine-mfr', 'weapon-fire-into-occ-veh', 'homicide-other', 'drug-hallucinogen-possess', 'violation-of-restraining-order', 'property-crimes-other', 'menacing-felony-w-weap', 'traf-vehicular-assault', 'theft-items-from-vehicle', 'theft-from-mails', 'sex-aslt-fondle-adult-victim', 'fraud-by-telephone', 'theft-of-motor-vehicle', 'stolen-property-buy-sell-rec', 'agg-aslt-police-weapon', 'robbery-purse-snatch-w-force', 'burg-auto-theft-busn-no-force', 'assault-police-simple', 'fraud-nsf-closed-account', 'theft-of-services', 'drug-heroin-sell', 'burglary-poss-of-tools', 'weapon-fire-into-occ-bldg', 'sex-aslt-rape', 'forgery-checks', 'fraud-criminal-impersonation', 'public-order-crimes-other', 'prostitution-engaging-in', 'burglary-residence-by-force', 'assault-simple', 'drug-cocaine-sell', 'theft-bicycle', 'animal-cruelty-to', 'arson-residence', 'traf-habitual-offender', 'drug-synth-narcotic-possess', 'police-resisting-arrest', 'kidnap-adult-victim', 'drug-make-sell-other-drug', 'burglary-vending-machine', 'police-obstruct-investigation', 'weapon-flourishing', 'drug-marijuana-sell', 'intimidation-of-a-witness', 'extortion', 'harassment-stalking-dv', 'robbery-business', 'burglary-business-no-force', 'contraband-into-prison', 'contraband-possession', 'traf-impound-vehicle', 'drug-heroin-possess', 'police-interference', 'theft-embezzle', 'explosive-incendiary-dev-pos', 'robbery-residence', 'theft-stln-vehicle-trailer']
keys = ['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION','OFFENSE_TYPE_ID','OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE','LAST_OCCURRENCE_DATE','REPORTED_DATE','INCIDENT_ADDRESS','GEO_X','GEO_Y','GEO_LON','GEO_LAT','DISTRICT_ID','PRECINCT_ID','NEIGHBORHOOD_ID']
neighborhoods = ['wellshire', 'bear-valley', 'hilltop', 'cbd', 'university-hills', 'overland', 'speer', 'union-station', 'washington-virginia-vale', 'marston', 'north-capitol-hill', 'city-park', 'sloan-lake', 'five-points', 'sun-valley', 'westwood', 'cole', 'windsor', 'platt-park', 'jefferson-park', 'harvey-park', 'skyland', 'sunnyside', 'southmoor-park', 'ruby-hill', 'capitol-hill', 'barnum-west', 'harvey-park-south', 'dia', 'athmar-park', 'elyria-swansea', 'lowry-field', 'goldsmith', 'stapleton', 'chaffee-park', 'berkeley', 'washington-park', 'indian-creek', 'barnum', 'montbello', 'civic-center', 'hampden-south', 'globeville', 'city-park-west', 'clayton', 'northeast-park-hill', 'country-club', 'hale', 'mar-lee', 'lincoln-park', 'gateway-green-valley-ranch', 'west-highland', 'congress-park', 'regis', 'east-colfax', 'whittier', 'belcaro', 'hampden', 'fort-logan', 'college-view-south-platte', 'montclair', 'baker', 'kennedy', 'cherry-creek', 'cheesman-park', 'west-colfax', 'south-park-hill', 'cory-merrill', 'rosedale', 'valverde', 'university-park', 'auraria', 'north-park-hill', 'highland', 'villa-park', 'university', 'virginia-village', 'washington-park-west']
populations = {'wellshire': '3133', 'cbd': '3648', 'university-hills': '5327', 'overland': '2218', 'speer': '10954', 'gateway-green-valley-ranch': '29201', 'ruby-hill': '9820', 'marston': '11132', 'north-capitol-hill': '5823', 'city-park': '2907', 'indian-creek': '3096', 'five-points': '12712', 'sun-valley': '1448', 'westwood': '15486', 'cole': '4651', 'washington-park-west': '6393', 'platt-park': '5393', 'harvey-park-south': '8393', 'villa-park': '8758', 'athmar-park': '8898', 'skyland': '3106', 'north-park-hill': '9382', 'sunnyside': '9726', 'southmoor-park': '3826', 'jefferson-park': '2552', 'capitol-hill': '14708', 'windsor': '12589', 'barnum-west': '5376', 'virginia-village': '12844', 'montbello': '30348', 'bear-valley': '8889', 'goldsmith': '5808', 'stapleton': '13948', 'chaffee-park': '3874', 'cory-merrill': '3892', 'northeast-park-hill': '7822', 'union-station': '4348', 'washington-park': '6905', 'barnum': '6111', 'elyria-swansea': '6401', 'civic-center': '1577', 'hampden-south': '14370', 'globeville': '3687', 'city-park-west': '4844', 'clayton': '4336', 'cheesman-park': '7971', 'country-club': '3001', 'hale': '6936', 'mar-lee': '12452', 'lincoln-park': '6119', 'berkeley': '8112', 'west-highland': '8540', 'harvey-park': '11525', 'regis': '3934', 'east-colfax': '10191', 'whittier': '4831', 'belcaro': '4172', 'hampden': '17547', 'fort-logan': '8532', 'college-view-south-platte': '6498', 'west-colfax': '9740', 'baker': '4879', 'kennedy': '4464', 'cherry-creek': '5589', 'dia': '1165', 'congress-park': '10235', 'south-park-hill': '8590', 'rosedale': '2553', 'valverde': '3941', 'lowry-field': '8067', 'washington-virginia-vale': '13030', 'auraria': '705', 'hilltop': '8190', 'highland': '8429', 'montclair': '5456', 'university': '9375', 'university-park': '7491', 'sloan-lake': '7238'}

def abstract_keys(key):
    # Take a key, return its CSV equivalent.
    # Used so we can use this for more than just Denver crime csv.
    pass

def get_location_list(location_type):
    pass
    return locations

def get_location_ranking(locations, crime_type):
    pass

def get_timespan_crimes(location = None, time_type = 'month', quantity = 'this',  *args, **kwargs):
    # Get crimes from a particular span of time
    pass

def check_date(value):
    # Check a date to see if it's valid. If not, throw error.
    return datetime.strptime(value, '%Y-%m-%d')

def check_datetime(value):
    # Check a datetime to see if it's valid. If not, throw error.
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

def get_specific_crime(crime, grep, location = None):
    # Indexes specific crime.
    # Example: Hey, among Drug & Alcohol abuses in cap hill, is meth more popular than coke?
    # Returns frequency for entire csv specified.
    # Also returns the # of days since the last crime.
    crimes = get_recent_crimes(crime, grep, location)
    count = len(crimes)
    #print crimes[0], crimes[count-1]
    last_crime = None
    if count > 0:
        last_crime = crimes[count-1]['FIRST_OCCURRENCE_DATE']
    #for crime in crimes:
    #    print crime['OFFENSE_TYPE_ID']
    return { 'count': count, 'last_crime': last_crime }

def get_recent_crimes(crime = None, grep = False, location = None, *args, **kwargs):
    # Given a crime genre / cat / type, a location or a timespan, return a list of crimes.
    # Timespan is passed as an argument (start, finish)

    crimes = []

    if not args:
        timespan = None
    else:
        # timespan a tuple of dates, that defaults to everything.
        # Decided to set that here rather than in the method def for the sake of space.
        timespan = (datetime.date(datetime.strptime(args[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(args[0][1], '%Y-%m-%d')))
        if verbose:
            print "Publishing crimes from %s to %s" % ( timespan[0].month, timespan[1].month )

    crime_type = get_crime_type(crime)

    if verbose:
        print "Timespan: %s, loc: %s, crime: %s" % (timespan, location, crime)

    for row in crime_file:
        record = dict(zip(keys, row))
        

        # Time queries
        if timespan:
            ts = check_datetime(record['FIRST_OCCURRENCE_DATE'])
            if not timespan[0] <= datetime.date(ts) <= timespan[1]:
                continue

        # Location, then crime queries
        # This logic tree is more like four shrubs next to each other:
        # 1. No crime and no location parameters,
        # 2. Maybe crime, but yes location,
        # 3. No crime, yes location
        # 4. Yes crime, no location 
        if location == None and crime == None:
            crimes.append(record['OFFENSE_CATEGORY_ID'])
            continue

        if location != None and location != False:
            if record['NEIGHBORHOOD_ID'] != location:
                continue

        if crime == None:
            crimes.append(record['OFFENSE_CATEGORY_ID'])
            continue

        if crime != None:
            if crime_type == 'parent_category':
                if record['OFFENSE_CATEGORY_ID'] in crime_lookup_reverse[crime]:
                    crimes.append(record)
            else:
                if record[crime_type] == crime:
                    crimes.append(record)
                elif grep == True:
                    # Loop through the types of crimes 
                    # (the lowest-level crime taxonomy), 
                    # looking for a partial string match.
                    if crime in record['OFFENSE_TYPE_ID']:
                        crimes.append(record)
    return crimes


def get_crime_type(crime):
    # Figure out what type of crime we're querying
    # parent_category doesn't correspond to a CSV field,
    # which is why it looks different. So that's obvious.
    # type OFFENSE_TYPE_ID
    # genre violent / property / other 
    # category OFFENSE_CATEGORY_ID
    crime_type = 'OFFENSE_TYPE_ID'
    if crime in crime_genres:
        crime_type = 'parent_category'
    elif crime in crime_lookup:
        crime_type = 'OFFENSE_CATEGORY_ID'

    return crime_type


def get_rankings(crime = None, location = None, *args, **kwargs):
    # Take a crime type or category and return a list of neighborhoods 
    # ranked by frequency of that crime.
    # If no crime is passed, we just rank overall number of crimes
    # (and crimes per-capita) for that particular time period.
    # Args taken should be the start of the timespan and the end.
    rankings = { 
        'neighborhood': defaultdict(int),
        'genre': defaultdict(int),
        'category': defaultdict(int),
        'type': defaultdict(int)
    }
    percapita = { 
        'neighborhood': defaultdict(int),
        'genre': defaultdict(int),
        'category': defaultdict(int),
        'type': defaultdict(int)
    }
    percapita_multiplier = 1000
    today = datetime.date(datetime.now())
    timespan = (datetime.date(datetime.strptime(args[0][0], '%Y-%m-%d')), datetime.date(datetime.strptime(args[0][1], '%Y-%m-%d')))
    if not args:
        month = today - timedelta(90)
        timespan = (month, today)

    crime_type = get_crime_type(crime)

    for row in crime_file:
        record = dict(zip(keys, row))

        # Time queries
        ts = check_datetime(record['FIRST_OCCURRENCE_DATE'])
        if not timespan[0] <= datetime.date(ts) <= timespan[1]:
            continue

        if crime == None:
            # Update the neighborhood counter
            rankings['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
            percapita['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
            rankings['type'][record['OFFENSE_TYPE_ID']] += 1
            rankings['category'][record['OFFENSE_CATEGORY_ID']] += 1
            crime_genre = crime_lookup[record['OFFENSE_CATEGORY_ID']]
            rankings['genre'][crime_genre] += 1

        else:

            if crime == crime_lookup[record['OFFENSE_CATEGORY_ID']] or crime == record['OFFENSE_CATEGORY_ID'] or crime == record['OFFENSE_TYPE_ID']:
                #print crime, crime_lookup[record['OFFENSE_CATEGORY_ID']]
                rankings['neighborhood'][record['NEIGHBORHOOD_ID']] += 1
                percapita['neighborhood'][record['NEIGHBORHOOD_ID']] += 1

    for item in percapita['neighborhood'].items():
        #print "Item 1: %s Pop of %s: %s" % ( item[1], item[0], populations[item[0]] ), 
        percapita['neighborhood'][item[0]] = round( float(item[1])/float(populations[item[0]]) * 1000, 2)

    sorted_rankings = {
        'neighborhood': sorted(rankings['neighborhood'].iteritems(), key=operator.itemgetter(1)),
        'percapita': sorted(percapita['neighborhood'].iteritems(), key=operator.itemgetter(1)),
        'genre': sorted(rankings['genre'].iteritems(), key=operator.itemgetter(1)),
        'category': sorted(rankings['category'].iteritems(), key=operator.itemgetter(1)),
        'type': sorted(rankings['type'].iteritems(), key=operator.itemgetter(1))
    }
    return sorted_rankings

def get_median(ranking):
    # Take a ranking dict, add up the numbers, get the median.
    pass

def get_uniques(field):
    # Write a list of unique values from a field in the CSV
    values = []
    for row in crime_file:
        record = dict(zip(keys, row))
        values.append(record[field])

    print set(values)
    return set(values)

def get_neighborhood(location):
    # If location's in the list return that location name
    if location in neighborhoods:
        return location
    return False

def open_csv(fn = '_input/currentyear.csv'):
    # Open the crime file for parsing.
    # It defaults to the current year's file.
    fp = open(fn, 'rb')
    crime_file = csv.reader(fp, delimiter = ',')
    return crime_file


def print_crimes(crimes, limit):
    # How do we want to display the crimes?
    # Right now we're publishing them to be read in terminal.
    output = ''
    try:
        # Lists
        i = 0
        for crime in crimes[:limit]:
            i = i + 1
            output += '%i. %s' % (i, crime)
    except:
        # Dicts
        for key in crimes:
            output += "%s, %s\n" % (key, crimes[key])

    return output

if __name__ == '__main__':
    # Parse the arguments, pass 'em to the function
    # The three main args we use to query the crime data are
    # location, crime and timespan. location and crime are
    # passed as options, and timespan (start, finish) as the 
    # first two arguments. This may not be the best way to do it.
    parser = OptionParser()
    parser.add_option("-f", "--filename", dest="filename", default="currentyear.csv")
    parser.add_option("-a", "--action", dest="action")
    parser.add_option("-l", "--location", dest="location", default=None)
    parser.add_option("-t", "--limit", dest="limit", default=20)
    parser.add_option("-c", "--crime", dest="crime", default="violent")
    parser.add_option("-g", "--grep", dest="grep", default=False, action="store_true")
    parser.add_option("-y", "--yearoveryear", dest="yearoveryear", default=False, action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    (options, args) = parser.parse_args()
    filename = options.filename
    action = options.action
    location = options.location
    limit = options.limit
    crime = options.crime
    grep = options.grep
    yearoveryear = options.yearoveryear
    verbose = options.verbose

    location = get_neighborhood(location)

    if verbose:
        print "Options: %s\nArgs: %s" % (options, args)

    crime_file = open_csv("_input/%s" % filename)
    if action == 'rankings':
        # Example:
        # $ ./parse.py -a rankings -c violent '2013-01-01' '2013-02-01'
        crimes = get_rankings(crime, location, args)
        crimes['neighborhood'].reverse()
        crimes['percapita'].reverse()
    if action == 'recent':
        crimes = get_recent_crimes(crime, grep, location, args, {'test':options})
    if action == 'specific':
        # Example:
        # $ ./parse.py --verbose --action specific --crime drug-alcohol
        # $ ./parse.py --verbose --action specific --crime meth --grep True 
        crimes = get_specific_crime(crime, grep, location)
    print crimes
    print print_crimes(crimes, 15)
