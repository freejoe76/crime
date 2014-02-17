#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import math
from fancytext.fancytext import FancyText
from datetime import datetime

class TextBarchart():
    """ Takes a dict of key-values and returns a textual barchart such as this:
        𝙵𝙴𝙱 #### 208
        𝙹𝙰𝙽 ##### 260
        𝙳𝙴𝙲 #### 234
        𝙽𝙾𝚅 ####### 396
        𝙾𝙲𝚃 ##### 285
        𝚂𝙴𝙿 #### 212
        𝙰𝚄𝙶 ######## 443
        𝙹𝚄𝙻 ###### 301
        𝙹𝚄𝙽 ##### 293
        𝙼𝙰𝚈 ### 197
        𝙰𝙿𝚁 #### 240
        𝙼𝙰𝚁 ### 196
        """
    def __init__(self, options):
        """ Hey.
            """
        self.options = options

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

    def compute_mean(self, the_dict):
        """ Hey.
            """
        count = []
        for item in the_dict:
            count.append(item[1])
        return int(sum(count)/len(count))
        

    def compute_variance(self, the_dict):
        """ Hey.
            """
        count = []
        for item in the_dict:
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

    u = TextBarchart(options)
    for arg in args:
        print u.translate(arg), 

