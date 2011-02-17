#!/usr/bin/env python2.5

from rosettautil.optparse import OptionParser
from rosettautil.rosetta import rosettaScore

usage = "%prog [options] --term=scoreterm --percent=10 silent.out"
parser=OptionParser(usage)
parser.add_option("--term",dest="term",help="scoreterm to use")
parser.add_option("--percent",dest="percent",help="percent of structures to output",default=10)
(options,args) = parser.parse_args()

scores = rosettaScore.SilentScoreTable()
scores.add_file(args[0])

structure_count = len(scores)
percent = float(options.percent)/100.0
structs_to_print =int(percent*structure_count)

sorted_scores = scores.sorted_score_generator(options.term)

count = 0
while count < structs_to_print:
    (tag,score) = sorted_scores.next()
    print tag,score
    count += 1
