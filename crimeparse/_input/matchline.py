#!/usr/bin/env python
# If the seventh field in the input contains the date string that we're looking for, 
# output the entire line to stdout.
# The seventh field is FIRST_OCCURRENCE_DATE
from optparse import OptionParser
import re

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # First arg is the filename, second arg is the string we're looking for.
    search = re.compile(args[0])
    lines = open(args[1]).readlines()
    for line in lines:
        cells = line.split(',')
        # The seventh cell contains the date field we want to search.
        if search.search(cells[6]):
            if '\\' in line:
                line.replace('\\', '')
            print line.rstrip()
