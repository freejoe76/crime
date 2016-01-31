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

def test_monthly():
    #
    pass

def test_specific():
    # 
    parse = Parse('crimeparse/_input/test')
    parse.crime = 'violent'
    parse.grep = False
    result = parse.get_specific_crime()
    #assert result['crimes']['neighborhood'][0] == ('wellshire', {'count': 0, 'rank': 0})

def test_rankings():
    # Really should write something deeper than the existing doctests.
    parse = Parse('crimeparse/_input/test')
    parse.crime = 'violent'
    result = parse.get_rankings()
    assert result['crimes']['neighborhood'][0] == ('cbd', {'count': 3, 'rank': 0})
    assert result['crimes']['percapita'][50] == ('harvey-park-south', {'count': 0.0, 'rank': 0})
