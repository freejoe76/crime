#!/usr/bin/env python
# Run a spatial query against crime CSV's
import os
import csv
import operator
import shapely
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime, timedelta


class Within:
    """ class Within allows us to ask the crime CSV's
        spatial questions.
        This class when complete should be able to answer
        questions such as:

        1. Which crimes in this time period fell within the 
        boundaries of this shapefile?

        2. Which crimes fall with X miles of this point?
        """

    def __init__(self):
        pass

