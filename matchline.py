#!/usr/bin/env python
# If the seventh field in the input contains the date string that we're looking for, 
# output the entire line to stdout
import os
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    print args
    # First arg is the filename, second arg is the string we're looking for.
    lines = open(args[0]).readlines()
    for line in lines:
        cells = line.split(',')
        # The seventh cell contains the date field we want to search.
        if args[1] in cells[6]:
            print line
