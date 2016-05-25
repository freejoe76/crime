#!/usr/bin/env python
# Loop through the diff file and pull out the lines that were added.
# Note: Because of the way we diff it, "deleted" lines are the lines
# that are actually added.
#
# Output the lines we want to stdout.
# Here's a few lines from a diff file:
"""
2176d2175
< 20168020145.0,20168020145544100,5441,0,traffic-accident,traffic-accident,2016-05-18 17:26:00,,2016-05-18 18:10:00,7500 BLOCK PENA BLVD,3218193.0,1729463.0,-104.7230792,39.8336248,7,759,dia,0,1
2178,2179d2176
< 20168019966.0,20168019966529900,5299,0,weapon-other-viol,all-other-crimes,2016-05-17 18:04:59,,2016-05-17 18:40:00,8400 PENA BLVD,3231977.0,1735292.0,-104.6738123,39.8492917,7,759,dia,1,0
< 20168019902.0,20168019902240400,2404,0,theft-of-motor-vehicle,auto-theft,2016-04-04 21:59:00,2016-04-07 21:59:00,2016-05-17 11:35:59,23410 E 78TH AVE,3220587.0,1730733.0,-104.7145162,39.8370545,7,759,dia,1,0
2183d2179
< 20168019710.0,20168019710240400,2404,0,theft-of-motor-vehicle,auto-theft,2016-05-16 06:00:00,,2016-05-16 11:01:59,24530 E 78TH AVE,3224411.0,1730663.0,-104.7009023,39.8367708,7,759,dia,1,0
2196d2191
< 20168019117.0,20168019117230500,2305,0,theft-items-from-vehicle,theft-from-motor-vehicle,2016-04-18 18:00:00,2016-05-12 06:00:00,2016-05-12 11:03:00,25340 E 78TH AVE,3227061.0,1730870.0,-104.6914599,39.8372747,7,759,dia,1,0
2885c2880
"""
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # First arg is the filename, second arg is the string we're looking for.
    lines = open(args[0]).readlines()
    command = None
    for line in lines:
        if line[0] != '<' and line[0] != '>':
            if 'a' in line:
                command = 'add'
            elif 'c' in line:
                command = 'change'
            elif 'd' in line:
                command = 'delete'
            continue
        if command == 'add':
            continue
        elif command == 'change':
            continue
        elif command == 'delete':
            print line[2:].rstrip()
