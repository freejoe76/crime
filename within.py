#!/usr/bin/env python
# Run a spatial query against crime CSV's
import os
import csv
import operator
from collections import defaultdict
from optparse import OptionParser
from datetime import datetime, timedelta


class Within:
    """ class Within allows us to ask the crime CSV's
        spatial questions.
        """

    def __init__(self):
        pass

