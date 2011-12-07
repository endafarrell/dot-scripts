#!/usr/bin/python
import sys # for the command line arg processing
import getopt # for the command line arg processing
import math # for the log function

class Count2Cloud:

	fileName = ""
	base = float(10)
	multiplier = float(1)
	def __init__(self, fileName, base=float(10), multiplier=float(1)):
		self.fileName = fileName
		self.base = base
		self.multiplier = multiplier
		
	def run(self):
		f = open(self.fileName, 'r')
		lines = f.readlines()
		for line in lines:
			word, count = line.split(',')
			if int(count) > 1:
				log = math.log(float(count) * self.multiplier, self.base)
				for i in range(1, int(log)):
					print word,


def usage():
	print "Usage: word-count-log10-cloud"
	print " * [-h|--help]        get this help/usage message"
	print " * [-f|--file <url>]  the file to read from which WORD,COUNT is "
	print "                      converted to text with COUNT instances of "
	print "                      WORD (intended to be sent to sites like"
	print "                      converted to text with COUNT instances of "
	print "                      http://www.wordle.net/create"
	print "                         Edit: Remove numbers, Leave Words as"
	print "                           Spelled, Do Not Remove Common Words"
	print "                         Font: Teen"
	print "                         Layout: Rounder Edges, Mostly Horizontal"
	print "                         Color: Ghostly, A Little Variation"
	print "                      See the \"advanced\" which can take raw"
	print "                      data too!"
	print " * [-b|--base <base>] Optional log base (log10 is the default)"
	print " * [-m|--multiplier <m>] Optional count multiplier (PRE log)"

def main(argv):
	
	fileName = ""
	base = float(10)
	multiplier = float(1)
	try:
		opts, args = getopt.getopt(argv, "hf:b:m:", \
			["help", "file=", "base=", "multiplier="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--file"):
			fileName = arg
		elif opt in ("-b", "--base"):
			base = float(arg)
		elif opt in ("-m", "--multiplier"):
			multiplier = float(arg)
	if fileName == "":
		usage()
		print "Specify --file!"
		print argv
		sys.exit(2)
		sys.exit(2)
	ss = Count2Cloud(fileName, base, multiplier)
	ss.run()
	sys.exit(0)

if __name__ == "__main__":
	main(sys.argv[1:])