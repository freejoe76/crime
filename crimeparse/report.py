#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Publish json data suitable for a (week / month / quarter / year) report.
#
# Takes input (report time type, report location) and returns report in output type desired (json, text)


class Report:
    pass



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--type", dest="type")
    parser.add_option("-l", "--location", dest="location")
    parser.add_option("-o", "--output", dest="output", default="json")
    (options, args) = parser.parse_args()
