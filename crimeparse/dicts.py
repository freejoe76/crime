# Some information about how this all was put together would be useful.
crime_genres = ['violent', 'property', 'other']
crime_lookup_reverse = { 
    'violent': ['murder', 'robbery', 'aggravated-assault', 'sexual-assault'],
    'property': ['arson', 'theft-from-motor-vehicle', 'auto-theft', 'burglary', 'larceny'],
    'other': ['traffic-accident', 'all-other-crimes', 'drug-alcohol', 'other-crimes-against-persons', 'white-collar-crime', 'public-disorder'] 
    'traffic': ['traffic-accident']
}
crime_lookup = {
    'traffic-accident': 'traffic',
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
neighborhood_lookup = {
    'athmar-park': {'full': 'Athmar Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'auraria': {'full': 'Auraria', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'baker': {'full': 'Baker', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'barnum': {'full': 'Barnum', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'barnum-west': {'full': 'Barnum West', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'bear-valley': {'full': 'Bear Valley', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'belcaro': {'full': 'Belcaro', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'berkeley': {'full': 'Berkeley', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'capitol-hill': {'full': 'Capitol Hill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'cbd': {'full': 'CBD', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'chaffee-park': {'full': 'Chaffee Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'cheesman-park': {'full': 'Cheesman Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'cherry-creek': {'full': 'Cherry Creek', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'city-park': {'full': 'City Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'city-park-west': {'full': 'City Park West', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'civic-center': {'full': 'Civic Center', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'clayton': {'full': 'Clayton', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'cole': {'full': 'Cole', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'college-view-south-platte': {'full': 'College View South Platte', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'congress-park': {'full': 'Congress Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'cory-merrill': {'full': 'Cory Merrill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'country-club': {'full': 'Country Club', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'dia': {'full': 'DIA', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'east-colfax': {'full': 'East Colfax', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'elyria-swansea': {'full': 'Elyria Swansea', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'five-points': {'full': 'Five Points', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'fort-logan': {'full': 'Fort Logan', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'gateway-green-valley-ranch': {'full': 'Gateway Green Valley Ranch', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'globeville': {'full': 'Globeville', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'goldsmith': {'full': 'Goldsmith', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'hale': {'full': 'Hale', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'hampden': {'full': 'Hampden', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'hampden-south': {'full': 'Hampden South', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'harvey-park': {'full': 'Harvey Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'harvey-park-south': {'full': 'Harvey Park South', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'highland': {'full': 'Highland', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'hilltop': {'full': 'Hilltop', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'indian-creek': {'full': 'Indian Creek', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'jefferson-park': {'full': 'Jefferson Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'kennedy': {'full': 'Kennedy', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'lincoln-park': {'full': 'Lincoln Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'lowry-field': {'full': 'Lowry Field', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'mar-lee': {'full': 'Mar Lee', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'marston': {'full': 'Marston', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'montbello': {'full': 'Montbello', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'montclair': {'full': 'Montclair', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'north-capitol-hill': {'full': 'North Capitol Hill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'northeast-park-hill': {'full': 'Northeast Park Hill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'north-park-hill': {'full': 'North Park Hill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'overland': {'full': 'Overland', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'platt-park': {'full': 'Platt Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'regis': {'full': 'Regis', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'rosedale': {'full': 'Rosedale', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'ruby-hill': {'full': 'Ruby Hill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'skyland': {'full': 'Skyland', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'sloan-lake': {'full': 'Sloan Lake', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'southmoor-park': {'full': 'Southmoor Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'south-park-hill': {'full': 'South Park Hill', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'speer': {'full': 'Speer', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'stapleton': {'full': 'Stapleton', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'sunnyside': {'full': 'Sunnyside', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'sun-valley': {'full': 'Sun Valley', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'union-station': {'full': 'Union Station', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'university': {'full': 'University', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'university-hills': {'full': 'University Hills', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'university-park': {'full': 'University Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'valverde': {'full': 'Valverde', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'villa-park': {'full': 'Villa Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'virginia-village': {'full': 'Virginia Village', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'washington-park': {'full': 'Washington Park', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'washington-park-west': {'full': 'Washington Park West', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'washington-virginia-vale': {'full': 'Washington Virginia Vale', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'wellshire': {'full': 'Wellshire', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'west-colfax': {'full': 'West Colfax', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'west-colfax': {'full': 'West Colfax', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'west-highland': {'full': 'West Highland', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'westwood': {'full': 'Westwood', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'whittier': {'full': 'Whittier', 'nearest_neighbors': {}, 'location': {}, 'population': 0},
    'windsor': {'full': 'Windsor', 'nearest_neighbors': {}, 'location': {}, 'population': 0}
}

# Human-readable crime names.
crime_name_lookup = {
    'sovereign-treason-viol': 'Treason',
    'immigration-violations': 'Immigration violation',
    'homicide-family': 'Homicide by a family member',
    'hom-willful-kill-non-family-gu': 'Homicide by a stranger w/gun',
    'hom-willful-kill-nonfam-wp': 'Homicide by a stranger w/weapon',
    'homicide-police-by-gun': 'Homicide of a Police Officer w/gun',
    'homicide-police-weapon': 'Homicide of a Police Officer w/weapon',
    'homicide-negligent': 'Homicide by negligence',
    'hom-wilful-kill-gun': 'Homicide by gun',
    'homicide-other': 'Homicide by other means',
    'kidnap-minor-to-sex-aslt': 'Kidnap minor to sexually assault',
    'kidnap-adult-to-sex-aslt': 'Kidnap adult to sexually assault',
    'kidnap-juvenile-victim': 'Kidnap a minor',
    'kidnap-adult-victim': 'Kidnap an adult',
    'kidnap-dv': 'Domestic violence kidnapping',
    'kidnap-abduct-no-ransom-aslt': 'Abduction without ransom or assault',
    'kidnap-hijack-aircraft': 'Hijack an aircraft',
    'kidnap-parental': 'Kidnapping by parent',
    'kidnap-minor-nonparental': 'Kidnapping of a minor by non-parent',
    'false-imprisonment': 'False Imprisonment',
    'sex-aslt-gun': 'Rape, perpetrator had a gun',
    'sex-aslt-rape': 'Rape',
    'sex-aslt-rape-pot': 'Rape by a person in a position of trust',
    'sex-aslt-strong-arm': 'Rape using the threat of violence',
    'sex-aslt-non-rape': 'Unlawful sexual contact',
    'sex-aslt-non-rape-pot': 'Unlawful sexual contact',
    'sex-asslt-sodomy-boy-strng-arm': 'Sodomy of a male juvenile using bodily force',
    'sex-asslt-sodomy-man-strng-arm': 'Sodomy of an adult male using bodily force',
    'sex-asslt-sodomy-girl-strg-arm': 'Sodomy of a female juvenile using bodily force',
    'sex-asslt-sodomy-woman-str-arm': 'Sodomy of an adult female using bodily force',
    'sex-aslt-statutory-rape': 'Statutory rape',
    'sex-aslt-statutory-rape-pot': 'Statutory rape by a person in a position of trust',
    'sex-aslt-w-object': 'Sexual assault with an object',
    'sex-aslt-w-object-pot': 'Sexual assault w/object by a person in a position of trust',
    'robbery-business-gun': 'Robbery of a business using a gun',
    'robbery-business': 'Robbery of a business using a weapon',
    'robbery-busn-strong-arm': 'Robbery of a business using bodily force',
    'robbery-street-gun': 'Robbery of a person in the open using a gun',
    'robbery-street': 'Robbery of a person in the open',
    'robbery-street-strong-arm': 'Robbery of a person in the open using bodily force',
    'robbery-residence-gun': 'Robbery of a person in a residence using a gun',
    'robbery-residence': 'Robbery of a person in a residence',
    'robbery-resd-strong-arm': 'Robbery of a person in a residence using bodily force',
    'robbery-purse-snatch-w-force': 'Forcible Purse Snatching',
    'robbery-bank': 'Robbery of a bank',
    'robbery-car-jacking': 'Carjacking - armed',
    'robbery-other': 'Robbery - remarks',
    'aslt-agg-family-gun': 'Assault causing serious bodily injury by a family member using a gun',
    'aslt-agg-family-weapon': 'Assault causing serious bodily injury by a family member using a weapon',
    'agg-aslt-strong-arm-dv': 'Assault causing serious bodily injury using bodily force - domestic violence',
    'aslt-agg-non-family-gun': 'Assault causing serious bodily injury by a stranger using a gun',
    'aslt-agg-non-family-weapon': 'Assault causing serious bodily injury by a stranger using a weapon',
    'agg-aslt-strong-arm-nonfam': 'Assault causing serious bodily injury by a stranger using bodily force',
    'aslt-agg-police-gun': 'Assault causing serious bodily injury of a police officer using a gun',
    'agg-aslt-police-weapon': 'Assault causing serious bodily injury of a police officer using a weapon',
    'agg-aslt-police-ofc-stng-arm': 'Assault causing serious bodily injury of a police officer using bodily force',
    'assault-simple': 'Assault causing minor bodily injury',
    'assault-state': 'Assault causing minor bodily injury',
    'assault-dv': 'Assault causing minor bodily injury - domestic violence',
    'assault-police-simple': 'Assault causing minor bodily injury to a police officer',
    'agg-aslt-gun-other': 'Assault causing serious bodily injury using a gun',
    'weapon-fire-into-occ-veh': 'Weapon fired into an occupied vehicle',
    'weapon-fire-into-occ-bldg': 'Weapon fired into an occupied building',
    'aggravated-assault': 'Assault causing serious bodily injury',
    'aggravated-assault-dv': 'Assault causing serious bodily injury - domestic violence',
    'menacing-felony-w-weap': 'Threatening to imminently injure with a weapon',
    'weapon-flourishing': 'Flourishing a weapon at another person',
    'threats-to-injure': 'Threatening to injure',
    'harassment-stalking-dv': 'Harassment by stalking - domestic violence',
    'threats-city': 'Threatening to injure',
    'arson-business': 'Arson of a business',
    'arson-residence': 'Arson of a residence',
    'arson-other': 'Arson',
    'arson-public-building': 'Arson to a public building',
    'arson-vehicle': 'Arson of a vehicle',
    'extort-threat-inj-person': 'Extort-threaten to injure a person',
    'extortion': 'Extortion - other',
    'burglary-safe': 'Burglary of a safe',
    'burglary-residence-by-force': 'Burglary of a residence with forced entry',
    'burg-auto-theft-resd-w-force': 'Burglary and auto theft at a residence with forced entry',
    'burglary-business-by-force': 'Burglary of a business with forced entry',
    'burg-auto-theft-busn-w-force': 'Burglary and auto theft at a business with forced entry',
    'burglary-residence-no-force': 'Burglary of a residence without forced entry',
    'burg-auto-theft-resd-no-force': 'Burglary and auto theft at a residence without forced entry',
    'burglary-business-no-force': 'Burglary of a business without forced entry',
    'burg-auto-theft-busn-no-force': 'Burglary and auto theft at a business without forced entry',
    'burglary-poss-of-tools': 'Possession of burglary tools',
    'burglary-other': 'Burglary - other',
    'theft-pick-pocket': 'Pocketpicking',
    'theft-purse-snatch-no-force': 'Purse snatching without force',
    'theft-shoplift': 'Shoplifting',
    'theft-parts-from-vehicle': 'Theft of parts from a vehicle',
    'theft-items-from-vehicle': 'Theft of items from a vehicle',
    'burglary-vending-machine': 'Theft from a vending machine',
    'theft-from-bldg': 'Theft from a building',
    'theft-from-yards': 'Theft from a yard',
    'theft-from-mails': 'Theft from a mailbox',
    'larc-from-bank-type-inst': 'Theft from a bank',
    'theft-other': 'Theft - other',
    'theft-bicycle': 'Bicycle theft',
    'theft-gas-drive-off': 'Theft of fuel by driving off without paying',
    'theft-of-cable-services': 'Theft of cable services',
    'theft-stln-veh-const-eqpt': 'Theft of construction equipment',
    'theft-stln-vehicle-trailer': 'Theft of a trailer',
    'theft-vehicle-strip': 'Vehicle stolen and stripped',
    'theft-of-motor-vehicle': 'Motor vehicle theft',
    'theft-motor-veh-joy-ride': 'Unauthorized use of a vehicle or joy ride',
    'forgery-checks': 'Forgery of checks',
    'forgery-counterfeit-of-obj': 'Counterfeiting an object',
    'altering-vin-number': 'Altering a vehicle VIN number',
    'forgery-pass-forged-obj': 'Passing forged documents',
    'forg-pass-counterfeit-obj': 'Passing counterfeited objects (tickets, bonds, etc)',
    'forgery-poss-of-forged-inst': 'Possession of a forged instrument',
    'forgery-poss-of-forged-ftd': 'Possession of a forged financial transaction device (credit & debit cards)',
    'forg-poss-counterfeit-obj': 'Possession of counterfeited objects (tickets, bonds, etc)',
    'forgery-posses-forge-device': 'Possession of counterfeiting device',
    'forgery-other': 'Forgery - other',
    'drug-forgery-to-obtain': 'Forgery to obtain drugs',
    'theft-confidence-game': 'Theft by confidence game',
    'theft-of-rental-property': 'Theft of rental property',
    'theft-fail-return-rent-veh': 'Failure to return rental vehicle',
    'fraud-identity-theft': 'Identity theft',
    'fraud-criminal-impersonation': 'Criminal impersonation',
    'fraud-gather-id-info-deception': 'Gathering personal information by deception',
    'fraud-possess-id-theft-tools': 'Possession of identity theft tools',
    'impersonation-of-police': 'Police impersonation',
    'theft-unauth-use-of-ftd': 'Unauthorized use of a financial transaction device',
    'fraud-unauthorized-use-of-ftd': 'Unauthorized use of a financial transaction device',
    'fraud-nsf-closed-account': 'Fraud by check due to insufficient funds',
    'fraud-by-telephone': 'Fraud by telephone',
    'fraud-by-wire': 'Fraud by wire',
    'fraud-by-use-of-computer': 'Fraud by use of computer',
    'fraud-other': 'Fraud - other',
    'failure-to-pay-cab-fare': 'Failure to pay cab, bus or rail fare',
    'theft-of-meals': 'Theft of meals',
    'theft-of-services': 'Theft of services',
    'drug-fraud-to-obtain': 'Fraud to obtain drugs',
    'pawn-broker-viol': 'Pawn broker violation',
    'embezzle-bus-property': 'Embezzlement of business property',
    'theft-embezzle': 'Embezzlement by an employee',
    'stolen-property-sale-of': 'Sale of stolen property',
    'stolen-property-buy-sell-rec': 'Buy, sell or receive stolen property',
    'outside-steal-recovered-veh': 'Recovered vehicle stolen outside Denver',
    'stolen-property-possession': 'Possession of stolen property',
    'fraud-possess-financial-device': 'Possession of a financial device',
    'damaged-prop-bus': 'Damaged business property',
    'criminal-mischief-private': 'Criminal mischief to private property',
    'criminal-mischief-public': 'Criminal mischief to public property',
    'criminal-mischief-other': 'Criminal mischief - other',
    'criminal-mischief-mtr-veh': 'Criminal mischief to a motor vehicle',
    'criminal-mischief-graffiti': 'Criminal mischief - graffiti',
    'drug-hallucinogen-mfr': 'Manufacture of a hallucinogenic drug',
    'drug-hallucinogen-sell': 'Selling a hallucinogenic drug',
    'drug-hallucinogen-possess': 'Possession of a hallucinogenic drug',
    'drug-heroin-sell': 'Selling heroin',
    'drug-heroin-possess': 'Possession of heroin',
    'drug-opium-or-deriv-sell': 'Selling opium or an opium derivative',
    'drug-opium-or-deriv-possess': 'Possession of opium or an opium derivative',
    'drug-cocaine-sell': 'Selling cocaine',
    'drug-cocaine-possess': 'Possession of cocaine',
    'drug-synth-narcotic-sell': 'Selling a synthetic narcotic drug',
    'drug-synth-narcotic-possess': 'Possession of a synthetic narcotic drug',
    'drug-poss-paraphernalia': 'Possession of drug paraphernalia',
    'drug-marijuana-sell': 'Selling marijuana',
    'drug-marijuana-possess': 'Possession of marijuana',
    'drug-marijuana-cultivation': 'Cultivation of marijuana',
    'drug-methamphetamine-mfr': 'Manufacture of methampetamine',
    'drug-methampetamine-sell': 'Selling methampetamine',
    'drug-methampetamine-possess': 'Possession of methampetamine',
    'drug-barbiturate-mfr': 'Manufacture of a barbiturate',
    'drug-barbiturate-sell': 'Selling a barbiturate',
    'drug-barbiturate-possess': 'Possession of a barbiturate',
    'drug-pcs-other-drug': 'Other dangerous drugs - PCS',
    'drug-make-sell-other-drug': 'Manufacture or sell other dangerous drugs',
    'sex-aslt-fondle-adult-victim': 'Fondling of an adult',
    'indecent-exposure': 'Indecent exposure',
    'sex-off-incest-with-adult': 'Incest with an adult',
    'window-peeping': 'Window Peeping',
    'sex-off-fail-to-register': 'Failure to register as a sex offender',
    'sex-off-registration-viol': 'Sex offender registration violation',
    'indecent-exposure-to-adult': 'Indecent exposure to an adult',
    'sex-off-other': 'Sex offense - other',
    'obscene-material-possess': 'Possession of obscene material',
    'obscene-material-mfr': 'Manufacture of obscene material',
    'other-obscenity-crime': 'Other obscenity crime',
    'bigamy': 'Bigamy',
    'gambling-card-game-operating': 'Operating a gambling card game',
    'gambling-dice-game-operating': 'Operating a gambling dice game',
    'gambling-possess-gamb-device': 'Possession of a gambling device',
    'gambling-device': 'Running a gambling operation',
    'gambling-lottery-operating': 'Running an illegal lottery',
    'gambling-sports-tampering': 'Tampering with sports',
    'gambling-betting-wagering': 'Gambling - betting or wagering',
    'gambling-gaming-operation': 'Gambling - gaming operation',
    'gambling-illegal': 'Illegal gambling',
    'prostitution-keep-a-house-of': 'Keeping a house of prostitution',
    'prostitution-procure-for': 'Procure for prostitution (trafficking, operating a bordelo)',
    'prostitution-pimping': 'Pimping for prostitution',
    'prostitution-engaging-in': 'Engaging in prostitution',
    'prostitution': 'Prostitution',
    'prostitution-aiding': 'Aiding the act of prostitution',
    'prostituion-display-for': 'Display for prostitution',
    'liquor-manufacturing': 'Manufacture of liquor',
    'liquor-sell': 'Illegal sale of liquor',
    'liquor-possession': 'Illegal possession of liquor',
    'liquor-misrepresent-age-minor': 'Liquor law violation',
    'liquor-other-viol': 'Liquor law violation - other',
    'public-intoxication': 'Public intoxication',
    'police-resisting-arrest': 'Resisting arrest',
    'police-obstruct-investigation': 'Obstruction of a criminal investigation',
    'police-false-information': 'Giving false information to police',
    'police-making-a-false-rpt': 'Making a false report to police',
    'police-refusing-aid-to': 'Refusing to aid an officer',
    'failure-to-report-abuse': 'Failure to report abuse',
    'police-disobey-lawful-order': 'Failure to obey a lawful order by police',
    'police-interference': 'Obstructing police',
    'escape': 'Escape of a prisoner',
    'escape-aiding': 'Aiding the escape of a prisoner',
    'escape-other': 'Escape or flight',
    'intimidation-of-a-witness': 'Intimidation of a witness',
    'obstruct-jud-court-order-vio': 'Obstructing a court order',
    'parole-violation': 'Parole violation',
    'probation-violation': 'Probation violation',
    'failure-to-appear': 'Failure to appear',
    'violation-of-restraining-order': 'Violation of a restraining order',
    'violation-of-court-order': 'Violation of a court order',
    'violation-of-custody-order': 'Violation of a court order',
    'obstructing-govt-operation': 'Obstruction of a government operation',
    'bribery': 'Bribery',
    'weapon-altering-serial-number': 'Altering the serial number',
    'weapon-carrying-concealed': 'Carrying a concealed weapon',
    'weapon-carrying-prohibited': 'Carrying a prohibited weapon',
    'explosive-incendiary-dev-use': 'Using an explosive/incendiary device',
    'explosives-posses': 'Possession of an explosive',
    'explosive-incendiary-dev-pos': 'Possession of an explosive/incendiary device',
    'weapon-poss-illegal-dangerous': 'Possession of an illegal/dangerous weapon',
    'weapon-by-prev-offender-powpo': 'Possession of a weapon - POWPO',
    'weapon-unlawful-discharge-of': 'Unlawful discharge of a weapon',
    'weapon-flourishing': 'Flourishing of a weapon',
    'weapon-unlawful-sale': 'Unlawful sale of a weapon',
    'bomb-threat': 'Bomb threat',
    'weapon-other-viol': 'Weapon - other',
    'riot-incite': 'Inciting a riot',
    'riot': 'Engaging in a riot',
    'police-interference': 'Police Interference',
    'riot-unlawful-assembly': 'Unlawful assembly',
    'harassment': 'Harassment',
    'harassment-dv': 'Harassment - DV',
    'harassment-obscene': 'Obscene harassment',
    'harassment-sexual-in-nature': 'Harassment - sexual in nature',
    'pub-peace-desecrate-symb': 'Desecrating the flag',
    'public-fighting': 'Public fighting',
    'disturbing-the-peace': 'Disturbing the peace',
    'curfew': 'Curfew',
    'loitering': 'Loitering',
    'public-peace-vagrancy': 'Vagrancy',
    'public-peace-other': 'Public peace - other',
    'traf-habitual-offender': 'Habitual traffic offender',
    'traf-vehicular-homicide': 'Vehicular homicide',
    'traf-impound-vehicle': 'Impound abandoned vehicle on right-of-way',
    'traf-vehicular-assault': 'Vehicular assault',
    'traf-other': 'Traffic offense - other',
    'vehicular-eluding': 'Vehicular eluding',
    'vehicular-eluding-no-chase': 'Vehicular eluding - no chase',
    'health-violations': 'Health & safety violations',
    'eavesdropping': 'Eavesdropping',
    'criminal-trespassing': 'Criminal trespassing',
    'wiretapping': 'Wiretapping',
    'contraband-possession': 'Possession of contraband',
    'contraband-into-prison': 'Smuggle contraband to prisoner',
    'election-law-violation': 'Election laws violation',
    'money-laundering': 'Money laundering',
    'tax-violations': 'Tax revenue violation',
    'animal-cruelty-to': 'Cruelty to animals',
    'illegal-dumping': 'Illegal dumping',
    'other-conservation-crime': 'Other conversation offense',
    'littering': 'Littering',
    'other-enviornment-animal-viol': 'Other environmental or animal offense',
    'animal-poss-of-dangerous': 'Possession of a dangerous animal',
    'money-laundering': 'Money laundering',
    'crimes-against-person-other': 'Crimes against a person - other',
    'homicide-solicitation': 'Solicitation to commit homicide',
    'reckless-endangerment': 'Reckless endangerment',
    'disarming-a-peace-officer': 'Disarming a peace officer',
    'homicide-accessory-to': 'Accessory to commit homicide',
    'property-crimes-other': 'Property crimes - other',
    'property-crimes-other': 'Property crimes - other',
    'morals-other-moral-off': 'Morals / decency offense - other',
    'public-order-crimes-other': 'Public order offense - other',
    'fireworks-possession': 'Possession of fireworks',
    'public-order-crimes-other': 'Public order offense - other',
    'accessory-conspiracy-to-crime': 'Accessory / conspiracy to crime'
}

# Here so we can reference URLS such as http://denvercrimes.com/caphill 
# and redirect requests to an actual page.
neighborhood_shortcut_lookup = {
    'athmar-park': 'athmar-park',
    'auraria': 'auraria',
    'baker': 'baker',
    'barnum': 'barnum',
    'barnum-west': 'barnum-west',
    'bear-valley': 'bear-valley',
    'belcaro': 'belcaro',
    'berkeley': 'berkeley',
    'caphill': 'capitol-hill',
    'cbd': 'cbd',
    'chaffee-park': 'chaffee-park',
    'cheesman-park': 'cheesman-park',
    'cherry-creek': 'cherry-creek',
    'city-park': 'city-park',
    'city-park-west': 'city-park-west',
    'civic-center': 'civic-center',
    'clayton': 'clayton',
    'cole': 'cole',
    'college-view-south-platte': 'college-view-south-platte',
    'congress-park': 'congress-park',
    'cory-merrill': 'cory-merrill',
    'dia': 'dia',
    'east-colfax': 'east-colfax',
    'elyria-swansea': 'elyria-swansea',
    'five-points': 'five-points',
    'gateway-green-valley-ranch': 'gateway-green-valley-ranch',
    'globeville': 'globeville',
    'goldsmith': 'goldsmith',
    'hale': 'hale',
    'hampden': 'hampden',
    'hampden-south': 'hampden-south',
    'harvey-park': 'harvey-park',
    'harvey-park-south': 'harvey-park-south',
    'highland': 'highland',
    'hilltop': 'hilltop',
    'indian-creek': 'indian-creek',
    'jefferson-park': 'jefferson-park',
    'kennedy': 'kennedy',
    'lincoln-park': 'lincoln-park',
    'lowry-field': 'lowry-field',
    'mar-lee': 'mar-lee',
    'marston': 'marston',
    'montbello': 'montbello',
    'montclair': 'montclair',
    'north-capitol-hill': 'north-capitol-hill',
    'northeast-park-hill': 'northeast-park-hill',
    'north-park-hill': 'north-park-hill',
    'overland': 'overland',
    'platt-park': 'platt-park',
    'regis': 'regis',
    'ruby-hill': 'ruby-hill',
    'skyland': 'skyland',
    'sloan-lake': 'sloan-lake',
    'southmoor-park': 'southmoor-park',
    'south-park-hill': 'south-park-hill',
    'speer': 'speer',
    'stapleton': 'stapleton',
    'sunnyside': 'sunnyside',
    'sun-valley': 'sun-valley',
    'union-station': 'union-station',
    'university-hills': 'university-hills',
    'university-park': 'university-park',
    'university': 'university',
    'valverde': 'valverde',
    'villa-park': 'villa-park',
    'virginia-village': 'virginia-village',
    'washington-park-west': 'washington-park-west',
    'washington-virginia-vale': 'washington-virginia-vale',
    'wellshire': 'wellshire',
    'west-colfax': 'west-colfax',
    'west-highland': 'west-highland',
    'westwood': 'westwood',
    'whittier': 'whittier',
    'windsor': 'windsor'
}
crime_types = ['criminal-mischief-mtr-veh', 'burglary-residence-no-force', 'vehicular-eluding-no-chase', 'traf-other', 'aslt-agg-police-gun', 'weapon-unlawful-discharge-of', 'theft-other', 'forgery-other', 'drug-barbiturate-possess', 'robbery-car-jacking', 'forgery-poss-of-forged-inst', 'failure-to-appear', 'theft-stln-veh-const-eqpt', 'arson-vehicle', 'liquor-possession', 'robbery-bank', 'other-enviornment-animal-viol', 'sex-aslt-non-rape', 'police-false-information', 'pawn-broker-viol', 'drug-methampetamine-possess', 'criminal-mischief-graffiti', 'burglary-business-by-force', 'weapon-carrying-concealed', 'harassment-dv', 'forgery-counterfeit-of-obj', 'drug-opium-or-deriv-sell', 'aggravated-assault', 'drug-cocaine-possess', 'robbery-street', 'theft-unauth-use-of-ftd', 'sex-off-fail-to-register', 'weapon-other-viol', 'violation-of-custody-order', 'theft-parts-from-vehicle', 'window-peeping', 'escape', 'violation-of-court-order', 'harassment', 'drug-fraud-to-obtain', 'criminal-mischief-other', 'theft-pick-pocket', 'bomb-threat', 'drug-hallucinogen-sell', 'aggravated-assault-dv', 'burglary-safe', 'arson-other', 'drug-poss-paraphernalia', 'theft-fail-return-rent-veh', 'theft-gas-drive-off', 'weapon-carrying-prohibited', 'weapon-by-prev-offender-powpo', 'theft-from-bldg', 'criminal-trespassing', 'liquor-misrepresent-age-minor', 'police-disobey-lawful-order', 'fraud-by-use-of-computer', 'burg-auto-theft-resd-w-force', 'drug-pcs-other-drug', 'drug-methampetamine-sell', 'burg-auto-theft-busn-w-force', 'impersonation-of-police', 'drug-marijuana-possess', 'theft-shoplift', 'assault-dv', 'fraud-identity-theft', 'theft-purse-snatch-no-force', 'drug-forgery-to-obtain', 'kidnap-dv', 'false-imprisonment', 'illegal-dumping', 'disturbing-the-peace', 'burg-auto-theft-resd-no-force', 'obstructing-govt-operation', 'public-fighting', 'police-making-a-false-rpt', 'weapon-poss-illegal-dangerous', 'indecent-exposure', 'harassment-sexual-in-nature', 'threats-to-injure', 'fireworks-possession', 'vehicular-eluding', 'drug-methamphetamine-mfr', 'weapon-fire-into-occ-veh', 'homicide-other', 'drug-hallucinogen-possess', 'violation-of-restraining-order', 'property-crimes-other', 'menacing-felony-w-weap', 'traf-vehicular-assault', 'theft-items-from-vehicle', 'theft-from-mails', 'sex-aslt-fondle-adult-victim', 'fraud-by-telephone', 'theft-of-motor-vehicle', 'stolen-property-buy-sell-rec', 'agg-aslt-police-weapon', 'robbery-purse-snatch-w-force', 'burg-auto-theft-busn-no-force', 'assault-police-simple', 'fraud-nsf-closed-account', 'theft-of-services', 'drug-heroin-sell', 'burglary-poss-of-tools', 'weapon-fire-into-occ-bldg', 'sex-aslt-rape', 'forgery-checks', 'fraud-criminal-impersonation', 'public-order-crimes-other', 'prostitution-engaging-in', 'burglary-residence-by-force', 'assault-simple', 'drug-cocaine-sell', 'theft-bicycle', 'animal-cruelty-to', 'arson-residence', 'traf-habitual-offender', 'drug-synth-narcotic-possess', 'police-resisting-arrest', 'kidnap-adult-victim', 'drug-make-sell-other-drug', 'burglary-vending-machine', 'police-obstruct-investigation', 'weapon-flourishing', 'drug-marijuana-sell', 'intimidation-of-a-witness', 'extortion', 'harassment-stalking-dv', 'robbery-business', 'burglary-business-no-force', 'contraband-into-prison', 'contraband-possession', 'traf-impound-vehicle', 'drug-heroin-possess', 'police-interference', 'theft-embezzle', 'explosive-incendiary-dev-pos', 'robbery-residence', 'theft-stln-vehicle-trailer']
keys = ['INCIDENT_ID','OFFENSE_ID','OFFENSE_CODE','OFFENSE_CODE_EXTENSION','OFFENSE_TYPE_ID','OFFENSE_CATEGORY_ID','FIRST_OCCURRENCE_DATE','LAST_OCCURRENCE_DATE','REPORTED_DATE','INCIDENT_ADDRESS','GEO_X','GEO_Y','GEO_LON','GEO_LAT','DISTRICT_ID','PRECINCT_ID','NEIGHBORHOOD_ID']
neighborhoods = ['wellshire', 'bear-valley', 'hilltop', 'cbd', 'university-hills', 'overland', 'speer', 'union-station', 'washington-virginia-vale', 'marston', 'north-capitol-hill', 'city-park', 'sloan-lake', 'five-points', 'sun-valley', 'westwood', 'cole', 'windsor', 'platt-park', 'jefferson-park', 'harvey-park', 'skyland', 'sunnyside', 'southmoor-park', 'ruby-hill', 'capitol-hill', 'barnum-west', 'harvey-park-south', 'dia', 'athmar-park', 'elyria-swansea', 'lowry-field', 'goldsmith', 'stapleton', 'chaffee-park', 'berkeley', 'washington-park', 'indian-creek', 'barnum', 'montbello', 'civic-center', 'hampden-south', 'globeville', 'city-park-west', 'clayton', 'northeast-park-hill', 'country-club', 'hale', 'mar-lee', 'lincoln-park', 'gateway-green-valley-ranch', 'west-highland', 'congress-park', 'regis', 'east-colfax', 'whittier', 'belcaro', 'hampden', 'fort-logan', 'college-view-south-platte', 'montclair', 'baker', 'kennedy', 'cherry-creek', 'cheesman-park', 'west-colfax', 'south-park-hill', 'cory-merrill', 'rosedale', 'valverde', 'university-park', 'auraria', 'north-park-hill', 'highland', 'villa-park', 'university', 'virginia-village', 'washington-park-west']
populations = {'wellshire': '3133', 'cbd': '3648', 'university-hills': '5327', 'overland': '2218', 'speer': '10954', 'gateway-green-valley-ranch': '29201', 'ruby-hill': '9820', 'marston': '11132', 'north-capitol-hill': '5823', 'city-park': '2907', 'indian-creek': '3096', 'five-points': '12712', 'sun-valley': '1448', 'westwood': '15486', 'cole': '4651', 'washington-park-west': '6393', 'platt-park': '5393', 'harvey-park-south': '8393', 'villa-park': '8758', 'athmar-park': '8898', 'skyland': '3106', 'north-park-hill': '9382', 'sunnyside': '9726', 'southmoor-park': '3826', 'jefferson-park': '2552', 'capitol-hill': '14708', 'windsor': '12589', 'barnum-west': '5376', 'virginia-village': '12844', 'montbello': '30348', 'bear-valley': '8889', 'goldsmith': '5808', 'stapleton': '13948', 'chaffee-park': '3874', 'cory-merrill': '3892', 'northeast-park-hill': '7822', 'union-station': '4348', 'washington-park': '6905', 'barnum': '6111', 'elyria-swansea': '6401', 'civic-center': '1577', 'hampden-south': '14370', 'globeville': '3687', 'city-park-west': '4844', 'clayton': '4336', 'cheesman-park': '7971', 'country-club': '3001', 'hale': '6936', 'mar-lee': '12452', 'lincoln-park': '6119', 'berkeley': '8112', 'west-highland': '8540', 'harvey-park': '11525', 'regis': '3934', 'east-colfax': '10191', 'whittier': '4831', 'belcaro': '4172', 'hampden': '17547', 'fort-logan': '8532', 'college-view-south-platte': '6498', 'west-colfax': '9740', 'baker': '4879', 'kennedy': '4464', 'cherry-creek': '5589', 'dia': '1165', 'congress-park': '10235', 'south-park-hill': '8590', 'rosedale': '2553', 'valverde': '3941', 'lowry-field': '8067', 'washington-virginia-vale': '13030', 'auraria': '705', 'hilltop': '8190', 'highland': '8429', 'montclair': '5456', 'university': '9375', 'university-park': '7491', 'sloan-lake': '7238'}

