#!/usr/bin/env python2.5
from optparse import OptionParser
from rosetta import rosettaScore
import sys

usage = "%prog [options] --x_axis=scoreterm --y_axis=scoreterm --silent=silent_file.out output_table.txt"
parser = OptionParser(usage)
parser.add_option("--x_axis",dest="x_axis",help="score term to plot on x axis")
parser.add_option("--y_axis",dest="y_axis",help="score term to plot on y axis")
parser.add_option("--silent",dest="silent",help="path to silent file",default="")
parser.add_option("--pdbs",dest="pdb_list",help="path to list fo pdb files",default="")
(options,args) = parser.parse_args()

if options.silent == "" and options.pdb_list == "":
    parser.error("you must specify --silent or --pdbs")

data = [] #list of tuples in form (tag,x_score,y_score)

if options.silent != "":
    scores = rosettaScore.SilentScoreTable()
    scores.add_file(options.silent)
    x_axis_scores = scores.score_generator(options.x_axis)
    y_axis_scores = scores.score_generator(options.y_axis)
    for x_point, y_point in zip(x_axis_scores,y_axis_scores):
        x_tag= x_point[0]
        y_tag = y_point[0]
        if x_tag != y_tag:
            sys.exit("tags aren't equal, something is very wrong")
        data.append( (x_tag,x_point[1],y_point[1]) )

if options.pdb_list != "":
    pdb_list = open(options.pdb_list,"rU")
    for pdb in pdb_list:
        scores = rosettaScore.ScoreTable(pdb.rstrip())
        x_score = scores.get_score(0,options.x_axis) #residue 0 is the total energy for the pose
        y_score = scores.get_score(0,options.y_axis) #residue 0 is the total energy for the pose
        data.append( (pdb,x_score,y_score) )
    pdb_list.close()

#now we have the data, so we output it
output_file = open(args[0],'w')
output_file.write("tag\t"+options.x_axis+"\t"+options.y_axis+"\n")
for tag,x_score,y_score in data:
    output_file.write(tag+"\t"+str(x_score)+"\t"+str(y_score)+"\n")
output_file.close()
