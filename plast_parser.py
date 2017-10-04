#! /usr/bin/env python

# plast_parser.py
# This takes a plast output format -2 and retrieves the description from the NCBI index file

import subprocess, sys, os

# print the help and exit the programm

def getHelp() :
	print """plastparse
	Usage : python plast_parser.py input_file.txt
	
	input_file.txt is output from Plast using outfmt -2
	"""
	sys.exit()

# Is the first argument a call for help ? or is there the amount of required arguments ?

if len(sys.argv)!=2 :
	getHelp()
if sys.argv[1] == "-h" :
	getHelp()
if sys.argv[1] == "--help" :
	getHelp()

infile = sys.argv[1]

#Does the file exist ?
if not os.path.isfile(infile) :
	print infile, " can't be found \n"
	getHelp()

outfile = '%s_parsed.txt' %(infile[:-4])

opened = open(infile, 'r')
openedOut = open(outfile, 'w')

colnames = "Query Name\tQuery Length\tSubject Name\tSubject Length\tAlignment Length\tQuery Start\tQuery End\tSubject start\tSubject end\tHsp Score\tHsp Expect\tPercent Match\tNumber_of_gaps\n"
openedOut.write(colnames)

for line in opened:
	lineParsed = line.split('\t')
	entry = lineParsed[1].split('|')[3]
	output = subprocess.check_output("blastdbcmd -db /scratch/db/nr/blastDB/nr -dbtype prot -entry '" + entry + "'", shell=True)
	record2 = output.split(' ',1)[1].split('\n',1)[0]
	record2 = record2.split(']',1)
	if len(record2) > 1:
		record2 = record2[0] + "]"
	else:
		record2 = record2[0]
	results = (lineParsed[0] + '\t' + lineParsed[12] + '\t'+ lineParsed[1] + record2 +
	'\t'+ lineParsed[17] + '\t'+ lineParsed[3] + '\t'+ lineParsed[6] + 
	'\t'+ lineParsed[7] + '\t'+ lineParsed[8] + '\t'+ lineParsed[9] + '\t'
	+ lineParsed[11] + '\t'+ lineParsed[10] + '\t'
	+ lineParsed[2] + '\t'+ lineParsed[5] + '\n')
	openedOut.write(results)
print "done"

opened.close() 
openedOut.close()
