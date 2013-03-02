# Dicts and lists and lists and dicts.
# These dicts are global.
crime_genres = ['violent', 'property', 'other']

# These dicts are property-specific
keymap = {
    'id': 'INCIDENT_ID',
    'type': 'OFFENSE_TYPE_ID',
    'category': 'OFFENSE_CATEGORY_ID',
    'date': 'FIRST_OCCURENCE_DATE',
    'date_reported': 'REPORTED_DATE',
    'lat': 'GEO_LAT',
    'lon': 'GEO_LON',
    'address': 'INCIDENT_ADDRESS',
    'location_neighborhood': 'NEIGHBORHOOD_ID',
}
keys = ['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION','OFFENSE_TYPE_ID','OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE','LAST_OCCURRENCE_DATE','REPORTED_DATE','INCIDENT_ADDRESS','GEO_X','GEO_Y','GEO_LON','GEO_LAT','DISTRICT_ID','PRECINCT_ID','NEIGHBORHOOD_ID']
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
neighborhoods = ['wellshire', 'bear-valley', 'hilltop', 'cbd', 'university-hills', 'overland', 'speer', 'union-station', 'washington-virginia-vale', 'marston', 'north-capitol-hill', 'city-park', 'sloan-lake', 'five-points', 'sun-valley', 'westwood', 'cole', 'windsor', 'platt-park', 'jefferson-park', 'harvey-park', 'skyland', 'sunnyside', 'southmoor-park', 'ruby-hill', 'capitol-hill', 'barnum-west', 'harvey-park-south', 'dia', 'athmar-park', 'elyria-swansea', 'lowry-field', 'goldsmith', 'stapleton', 'chaffee-park', 'berkeley', 'washington-park', 'indian-creek', 'barnum', 'montbello', 'civic-center', 'hampden-south', 'globeville', 'city-park-west', 'clayton', 'northeast-park-hill', 'country-club', 'hale', 'mar-lee', 'lincoln-park', 'gateway-green-valley-ranch', 'west-highland', 'congress-park', 'regis', 'east-colfax', 'whittier', 'belcaro', 'hampden', 'fort-logan', 'college-view-south-platte', 'montclair', 'baker', 'kennedy', 'cherry-creek', 'cheesman-park', 'west-colfax', 'south-park-hill', 'cory-merrill', 'rosedale', 'valverde', 'university-park', 'auraria', 'north-park-hill', 'highland', 'villa-park', 'university', 'virginia-village', 'washington-park-west']
populations = {'wellshire': '3133', 'cbd': '3648', 'university-hills': '5327', 'overland': '2218', 'speer': '10954', 'gateway-green-valley-ranch': '29201', 'ruby-hill': '9820', 'marston': '11132', 'north-capitol-hill': '5823', 'city-park': '2907', 'indian-creek': '3096', 'five-points': '12712', 'sun-valley': '1448', 'westwood': '15486', 'cole': '4651', 'washington-park-west': '6393', 'platt-park': '5393', 'harvey-park-south': '8393', 'villa-park': '8758', 'athmar-park': '8898', 'skyland': '3106', 'north-park-hill': '9382', 'sunnyside': '9726', 'southmoor-park': '3826', 'jefferson-park': '2552', 'capitol-hill': '14708', 'windsor': '12589', 'barnum-west': '5376', 'virginia-village': '12844', 'montbello': '30348', 'bear-valley': '8889', 'goldsmith': '5808', 'stapleton': '13948', 'chaffee-park': '3874', 'cory-merrill': '3892', 'northeast-park-hill': '7822', 'union-station': '4348', 'washington-park': '6905', 'barnum': '6111', 'elyria-swansea': '6401', 'civic-center': '1577', 'hampden-south': '14370', 'globeville': '3687', 'city-park-west': '4844', 'clayton': '4336', 'cheesman-park': '7971', 'country-club': '3001', 'hale': '6936', 'mar-lee': '12452', 'lincoln-park': '6119', 'berkeley': '8112', 'west-highland': '8540', 'harvey-park': '11525', 'regis': '3934', 'east-colfax': '10191', 'whittier': '4831', 'belcaro': '4172', 'hampden': '17547', 'fort-logan': '8532', 'college-view-south-platte': '6498', 'west-colfax': '9740', 'baker': '4879', 'kennedy': '4464', 'cherry-creek': '5589', 'dia': '1165', 'congress-park': '10235', 'south-park-hill': '8590', 'rosedale': '2553', 'valverde': '3941', 'lowry-field': '8067', 'washington-virginia-vale': '13030', 'auraria': '705', 'hilltop': '8190', 'highland': '8429', 'montclair': '5456', 'university': '9375', 'university-park': '7491', 'sloan-lake': '7238'}

