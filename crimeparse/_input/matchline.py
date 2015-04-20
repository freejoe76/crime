#!/usr/bin/env python
# If the seventh field in the input contains the date string that we're looking for, 
# output the entire line to stdout.
# The seventh field is FIRST_OCCURRENCE_DATE
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # First arg is the filename, second arg is the string we're looking for.
    lines = open(args[1]).readlines()
    for line in lines:
        cells = line.split(',')
        # The seventh cell contains the date field we want to search.
        if args[0] in cells[6]:
            print line.rstrip()
