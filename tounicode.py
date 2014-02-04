#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from optparse import OptionParser


class ToUnicode:
    """ Translate ascii to Unicode characters.
        >>> u = ToUnicode('TEST')
        >>> print u.translate()
        𝚃𝙴𝚂𝚃
        """

    def __init__(self, text):
        """ Translation matrix via Moses Moore (https://github.com/mozai/), http://mozai.com/programming/dandytype.html
            """
        self.translation = {
            'ascii':[["!",33,"~"]],
            'parens':[["A",9372,"Z"],["a",9372,"z"],["1",9332,"9"]],
            'circled':[["A",9398,"Z"],["a",9424,"z"],["0",9450,"0"],["1",9312,"9"]],
            'bold':[["A",119808,"Z"],["a",119834,"z"],["0",120782,"9"]],
            'italic':[["A",119860,"Z"],["a",119886,"z"]],
            'bolditalic':[["A",119912,"Z"],["a",119938,"z"]],
            'script':[["A",119964,"Z"],["a",119990,"z"]],
            'boldscript':[["A",120016,"Z"],["a",120042,"z"]],
            'fraktur':[["A",120068,"Z"],["a",120094,"z"]],
            'doublestruck':[["A",120120,"Z"],["a",120146,"z"],["0",120792,"9"]],
            'boldfraktur':[["A",120172,"Z"],["a",120198,"z"]],
            'sansserif':[["A",120224,"Z"],["a",120250,"z"],["0",120802,"9"]],
            'sserifbold':[["A",120276,"Z"],["a",120302,"z"],["0",120812,"9"]],
            'sserifitalic':[["A",120328,"Z"],["a",120354,"z"]],
            'sserifboldi':[["A",120380,"Z"],["a",120406,"z"]],
            'monospace':[["A",120432,"Z"],["a",120458,"z"],["0",120822,"9"]],
            'fullwidth':[["!",65281,"~"]]
        }
        self.text = text

    def translate(self, font='monospace'):
        """ First draft of a method to turn letters into monospace letters.
            What about other fonts? What about non-letter characters? That's later.
            """
        translated = ''
        if font not in self.translation:
            return False

        for i in self.text:
            chrnum = ord(i)
            if i.lower() == i:
                offset = 97
                print self.translation[1][1]
            elif i.upper() == i:
                offset = chrnum - 65
                translated += unichr(self.translation['monospace'][0][1] + offset)

        return translated

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    for arg in args:
        u = ToUnicode(arg)
        print u.translate()
