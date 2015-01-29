#!/usr/bin/env python
# Deletes the last comma from a string.
# We don't know if the comma will be at the end or near the end of a string.
from optparse import OptionParser
import os.path
import types

def delete_comma(value):
    """ Returns a string without its final comma."""
    items = value.split(',')
    last = items.pop()
    return '%s%s' % (','.join(items), last)

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    # Check if we're operating on the contents of a file
    if os.path.isfile(args[0]):
        fn = open(args[0], 'r')
        content = fn.read()
        fn.close
        fn = open(args[0], 'w')
        if type(content) is not types.UnicodeType:
            content = content.decode('utf-8', 'ignore')
        content = delete_comma(content)
        fn.write(content.encode('utf-8', 'ignore'))
        fn.close
    else:
        print delete_comma(' '.join(args))
