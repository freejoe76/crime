#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import math
from optparse import OptionParser
from fancytext.fancytext import FancyText
from datetime import datetime

class TextBarchart():
    """ Takes a dict of key-values and returns a textual barchart such as this:
        𝙹𝙰𝙽 ■ 61
        𝙳𝙴𝙲 ■■■■ 207
        𝙽𝙾𝚅 ■■■■ 225
        𝙾𝙲𝚃 ■■ 141
        𝚂𝙴𝙿 ■■■ 180
        𝙰𝚄𝙶 ■■■ 168
        𝙹𝚄𝙻 ■■■ 168
        𝙹𝚄𝙽 ■■■ 152
        𝙼𝙰𝚈 ■■■■■ 260
        𝙰𝙿𝚁 ■■■ 195
        𝙼𝙰𝚁 ■■■■ 208
        """
    def __init__(self, options, the_dict):
        """ Hey.
            """
        self.options = options
        self.the_dict = the_dict

    def find_max(self):
        """ Hey.
            """
        pass

    def compute_divisor(self, the_max):
        """ Hey.
            """
        if the_max > 80:
            divisor = 50
        if the_max > 800:
            divisor = 500
        if the_max > 8000:
            divisor = 5000
        return divisor

    def compute_mean(self):
        """ Hey.
            """
        count = []
        for item in self.the_dict:
            count.append(item[1])
        return int(sum(count)/len(count))
        

    def compute_variance(self):
        """ Hey.
            """
        count = []
        for item in self.the_dict:
            diff = item[1] - mean
            count.append(diff*diff)

        return int(sum(count)/len(count))

    def compute_deviation(self):
        """ Calculate the standard deviation.
            If the deviation's too low, there's no point in publishing the bar part of this chart.
            """
        return int(math.sqrt(self.variance))

    def build_chart(self):
        """ Hey.
            """

        self.mean = self.compute_mean(self.the_dict)
        self.variance = self.compute_variance(self.the_dict)
        self.deviation = self.compute_deviation()

        # *** Possible barchars: #,■,▮,O,☠
        barchar = u'☠'
        # If the deviation-to-mean ratio is more than 50%, that means
        # most of the values are close to the mean and we don't really
        # need a barchart.
        if float(self.deviation)/self.mean > .5:
            barchar = ''

        # We would like the date monospaced.
        font = FancyText()
        # *** We should have an option to allow for the year if we want it in this month-to-month
        date_format = '%b'
        for item in the_dict:
            values = {
                'date': font.translate(datetime.strftime(item[1]['date'], date_format).upper()),
                'count': item[1]['count'],
                'barchart': barchar*int(item[1]['count']/divisor)
            }
            outputs += u'%(date)s %(barchart)s %(count)s\n' % values

        return outputs


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--type", dest="type", default=None) # Date, String... not sure what the other types
    parser.add_option("-f", "--font", dest="font")
    (options, args) = parser.parse_args()

    # Need to figure out how to pass dict input via command line
    #bar = TextBarchart(options, args)
    #print bar.build_chart()
