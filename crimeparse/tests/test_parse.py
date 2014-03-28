#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from crimeparse.parse import Parse

def test_full():
    ''' # Not ready yet
    filename = 'currentyear'
    parse = Parse("_input/%s" % filename, diff, options)
    '''
    pass


class TestParse:

    def __init__(self):
        self.basedir = 'crimeparse'       
        self.basedir = '..'
        self.parse = Parse('%s/_input/test' % self.basedir)

    def test_monthly(self):
        #
        pass

    def test_specific(self):
        # 
        crime, grep = self.parse.set_crime('violent'), self.parse.set_grep(False)
        result = self.parse.get_specific_crime()
        assert result['crimes']['neighborhood'][0] == ('wellshire', {'count': 0, 'rank': 0})

    def test_rankings(self):
        # Really should write something deeper than the existing doctests.
        crime = self.parse.set_crime('violent')
        result = self.parse.get_rankings()
        assert result['crimes']['neighborhood'][0] == ('wellshire', {'count': 0, 'rank': 0})
        assert result['crimes']['percapita'][50] == ('west-colfax', {'count': 0.1, 'rank': 0})
