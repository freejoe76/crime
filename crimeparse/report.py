#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (week / month / quarter / year) report.
#
# Takes input (report time type, report location) and returns report in output type desired (json, text)
from optparse import OptionParser
from parse import Parse

class Report:
    """ class Report is an interface with class Parse to pull out defined 
        crime queries. How these crime queries will be defined... is up in the
        air. 
        """

    def __init__(self, type, location, output = 'json', options = None):
        # Initialize the major vars
        self.set_type(type)
        self.set_location(location)
        self.set_output(output)

    def set_type(self, value):
        """ Set the object's type var.
            >>> report = Report('month', 'capitol-hill')
            >>> type = report.set_type('quarter')
            >>> print type
            quarter
            """
        self.type = value
        return self.type

    def set_location(self, value):
        """ Set the object's location var.
            >>> report = Report('month', 'capitol-hill')
            >>> location = report.set_location('cbd')
            >>> print location
            cbd
            """
        self.location = value
        return self.location

    def set_output(self, value):
        """ Set the object's output var.
            >>> report = Report('month', 'capitol-hill')
            >>> output = report.set_output('text')
            >>> print output
            text
            """
        self.output = value
        return self.output



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--type", dest="type")
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-o", "--output", dest="output", default="json")
    (options, args) = parser.parse_args()
