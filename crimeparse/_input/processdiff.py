#!/usr/bin/env python
# Loop through the diff file and pull out the lines that were added.
# Output the lines we want to stdout.
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # First arg is the filename, second arg is the string we're looking for.
    lines = open(args[0]).readlines()
    command = None
    for line in lines:
        if line[0] != '<' and line[0] != '>':
            if 'a' in line:
                command = 'add'
            elif 'c' in line:
                command = 'change'
            elif 'd' in line:
                command = 'delete'
            continue
        if command == 'add':
            continue
        elif command == 'change':
            continue
        elif command == 'delete':
            print line[2:].rstrip()
