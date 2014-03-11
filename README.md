Crime
=====
A parser and logger for the City of Denver's crime CSV. Currently outputs to terminal. No database required.

![CrimeParse Tests](https://api.travis-ci.org/freejoe76/crime.png)

To get started with the first download and a view on a variety of reports:
    $ cd crimeparse
    $ ./ingest.bash
    $ ./report.bash --location capitol-hill

Taxonomy
========
There are three levels of crimes: 

1. Genre (violent / property / other)
2. Category (i.e. Drug & Alcohol)
3. Type (i.e. Drug: Cocaine Possession)

Usage
=====
Three major views exist:
Specifc
-------
This publishes frequency and last-occurence info about a particular type of crime in a particular neighborhood (optional).
### Example usage
    # Publish information about drug and alcohol crimes in the whole city:
    $ ./parse.py --action specific --crime drug-alcohol
    # Publish information about any crimes with "meth" in the name in the city:
    $ ./parse.py --action specific --crime meth --grep True 
    # Publish information about homicides in Capitol Hill
    $ ./parse.py --action specific --crime murder --location capitol-hill

Recent
------
Publish a list of recent crimes of a particular type and/or category, or genre. Can filter crimes by location and date.
### Example usage
    # Publish a list of drug and alcohol crimes in Capitol Hill
    $ ./parse.py --verbose --action recent --crime drug-alcohol --location capitol-hill
    # Publish a CSV of all violent crimes in Capitol Hill
    $ ./parse.py --action recent --crime violent --location capitol-hill --output csv

Rankings
--------
Publish per-capita and raw-number rankings for a crime type and/or category, or genre. Can filter by date.
### Example usage
    # Compare neighborhood violent crime rate in January:
    $ ./parse.py --action rankings --crime violent '2013-01-01' '2013-02-01'
