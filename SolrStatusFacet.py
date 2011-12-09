#!/usr/bin/python
try:
	import xml.etree.ElementTree as ET # in python >=2.5
except ImportError:
	try:
		import cElementTree as ET # effbot's C module
	except ImportError:
		try:
			import elementtree.ElementTree as ET # effbot's pure Python module
		except ImportError:
			try:
				import lxml.etree as ET # ElementTree API using libxml2
			except ImportError:
				import warnings
				warnings.warn("could not import ElementTree "
					"(http://effbot.org/zone/element-index.htm)")
				# Or you might just want to raise an ImportError here.
# Use ET.Element, ET.ElementTree, etc...
import json
import sys # For the cmd-line args and printing to stderr
import os.path # To check if the RRD file already exists
import os # To run the "create RRD file" command
import time # To calculate the seconds since epoch
import re # To better print the RRD commands

class SolrStatusFacet:
	
	dates = []
	actives = {}
	mergeds = {}
	removeds = {}
	BASEDIR = "."

	def __init__(self,):
		pass
	
	@staticmethod
	def sumData(dates, actives, mergeds, removeds):
		tA = 0
		tM = 0
		tR = 0
		summedData = {}
		for date in dates:
			tA = tA + actives[date]
			tM = tM + mergeds[date]
			tR = tR + removeds[date]
			summedData[date] = [tA, tM, tR]
		return summedData
	
	@staticmethod
	def date2Sec(date):
		return int(time.mktime(time.strptime(date, "%Y-%m-%d")))
	
	def run(self):		
		self.actives = self.readData("active.xml")
		self.mergeds = self.readData("merged.xml")
		self.removeds = self.readData("removed.xml")
		
		summedData = SolrStatusFacet.sumData(self.dates, self.actives,
			self.mergeds, self.removeds)
		self.dates.sort()
		for date in self.dates:
			if summedData[date][0] == 0:
				continue
			for delta in range(0, 86400, 300):
				cmd = "rrdtool update status-counts.rrd %d:%d:%d:%d" % (
					SolrStatusFacet.date2Sec(date) + delta,
					summedData[date][0],
					summedData[date][1], 
					summedData[date][2]
				)
				#print cmd
				os.system(cmd)

	def readData(self, fileName):
		dataHash = {}
		f = open(fileName, 'r')
		tree = ET.parse(f)
		
		lastModifieds = None
		lstElements = tree.findall(".//lst/lst/lst")
		for lstElement in lstElements:
			if lstElement.attrib["name"] == "lastmodifiedtime":
				lastModifieds = lstElement
				break
		ints = lastModifieds.findall("int")
		for intx in ints:
			date = intx.attrib["name"].split("T")[0]
			if not date in self.dates:
				self.dates.append(date)
			dataHash[date] = int(intx.text)
		return dataHash

	@staticmethod
	def createRRD():
		""" Here is the 45k RRD database definition:
		* 1151625600 == 2006-06-30 02:00:00 CEST
		*        300 == number of seconds in 5 minutes (our update script freq)
		*        900 == number of seconds in 15 minutes
		*        288 == number of 5 minute intervals in one day
		*       1825 == number of days in 5 years
		If an RRD file of the name status-counts.rrd is found in the 
		current dir, this script will not do anything to it and assume that
		the RRD file is good.
		"""
		if not os.path.isfile("status-counts.rrd"):
			cmd = "rrdtool create status-counts.rrd \
				--start 1151625600 --step 300 \
				DS:active:GAUGE:900:0:U \
				DS:merged:GAUGE:900:0:U \
				DS:removed:GAUGE:900:0:U \
				RRA:MAX:0.999:288:1825"
			pat = re.compile(r'\s+')
			print >> sys.stderr, "Creating RRD file using:\n%s" \
				% pat.sub(" ", cmd)
			os.system(cmd)
	
	def createPNG(self):
		cmd = "rrdtool graph statuses.png \
			--start=now-6month \
			--end=now \
			--step=300 \
			--title=\"Registry place statuses\" \
			--height=100 \
			--width=300 \
			--alt-autoscale-max \
			--lower-limit=0 \
			--slope-mode \
			--color CANVAS#EEEEEEFF \
			--color SHADEA#FFFFFFFF \
			--color SHADEB#FFFFFFFF \
			--color BACK#FFFFFFFF \
			--color FONT#000000FF \
			--color AXIS#000000FF \
			--legend-direction=bottomup \
			DEF:a=status-counts.rrd:active:MAX \
			DEF:m=status-counts.rrd:merged:MAX \
			DEF:r=status-counts.rrd:removed:MAX \
			CDEF:m2=m,-1,* \
			CDEF:r2=r,-1,* \
			AREA:a#009900AA:active \
			AREA:m2#000099AA:merged \
			STACK:r2#990000AA:removed \
			COMMENT:.\\\n \
			GPRINT:a:LAST:\"%.0lf active\" \
			GPRINT:m:LAST:\"%.0lf merged\" \
			GPRINT:r:LAST:\"%.0lf removed\" \
			COMMENT:.\\\n"
		os.system(cmd)
		cmd = "rrdtool graph %s/statuses.png \
			--start=now-6month \
			--end=now \
			--step=300 \
			--title=\"Registry place statuses\" \
			--height=100 \
			--width=300 \
			--alt-autoscale-max \
			--lower-limit=0 \
			--slope-mode \
			--color CANVAS#EEEEEEFF \
			--color SHADEA#FFFFFFFF \
			--color SHADEB#FFFFFFFF \
			--color BACK#FFFFFFFF \
			--color FONT#000000FF \
			--color AXIS#000000FF \
			DEF:a=%s/status-counts.rrd:active:MAX \
			DEF:m=%s/status-counts.rrd:merged:MAX \
			DEF:r=%s/status-counts.rrd:removed:MAX \
			CDEF:m2=m,-1,* \
			CDEF:r2=r,-1,* \
			AREA:a#009900AA:active \
			AREA:m2#000099AA:merged \
			STACK:r2#990000AA:removed \
			COMMENT:.\\\n \
			GPRINT:a:LAST:\"%%.0lf active\" \
			GPRINT:m:LAST:\"%%.0lf merged\" \
			GPRINT:r:LAST:\"%%.0lf removed\" \
			COMMENT:.\\\n" % (
				self.BASEDIR, self.BASEDIR, self.BASEDIR, self.BASEDIR)
		os.system(cmd)
		cmd = "rrdtool graph %s/status-active.png \
			--start=now-6month \
			--end=now \
			--step=300 \
			--title=\"Registry place statuses\" \
			--height=100 \
			--width=300 \
			--alt-autoscale-max \
			--slope-mode \
			--color CANVAS#EEEEEEFF \
			--color SHADEA#FFFFFFFF \
			--color SHADEB#FFFFFFFF \
			--color BACK#FFFFFFFF \
			--color FONT#000000FF \
			--color AXIS#000000FF \
			DEF:a=%s/status-counts.rrd:active:MAX \
			AREA:a#009900AA:active \
			COMMENT:.\\\n \
			GPRINT:a:LAST:\"%%.0lf active\" \
			COMMENT:.\\\n" % (
				self.BASEDIR, self.BASEDIR)
		os.system(cmd)
		cmd = "rrdtool graph %s/status-merged.png \
			--start=now-6month \
			--end=now \
			--step=300 \
			--title=\"Registry place statuses\" \
			--height=100 \
			--width=300 \
			--alt-autoscale-max \
			--slope-mode \
			--color CANVAS#EEEEEEFF \
			--color SHADEA#FFFFFFFF \
			--color SHADEB#FFFFFFFF \
			--color BACK#FFFFFFFF \
			--color FONT#000000FF \
			--color AXIS#000000FF \
			DEF:a=%s/status-counts.rrd:merged:MAX \
			AREA:a#009900AA:merged \
			COMMENT:.\\\n \
			GPRINT:a:LAST:\"%%.0lf merged\" \
			COMMENT:.\\\n" % (
				self.BASEDIR, self.BASEDIR)
		os.system(cmd)
		cmd = "rrdtool graph %s/status-removed.png \
			--start=now-6month \
			--end=now \
			--step=300 \
			--title=\"Registry place statuses\" \
			--height=100 \
			--width=300 \
			--alt-autoscale-max \
			--slope-mode \
			--color CANVAS#EEEEEEFF \
			--color SHADEA#FFFFFFFF \
			--color SHADEB#FFFFFFFF \
			--color BACK#FFFFFFFF \
			--color FONT#000000FF \
			--color AXIS#000000FF \
			DEF:a=%s/status-counts.rrd:removed:MAX \
			AREA:a#009900AA:removed \
			COMMENT:.\\\n \
			GPRINT:a:LAST:\"%%.0lf removed\" \
			COMMENT:.\\\n" % (
				self.BASEDIR, self.BASEDIR)
		os.system(cmd)
			

def usage():
	print "Usage:SolrStatusFacet.py"
	print " Reads the current dir for files called \"active.xml\", "
	print " \"merged.xml\" and \"removed.xml\". Builds a dict where the "
	print " key is a YYYY-MM-DD representation of the date and the value "
	print " is a list of integers representing the number of [active, merged"
	print " and removed] places."
	print "The data in the Solr responses is essentially the daily delta of"
	print " these statuses but we want to present the sum-totals at the"
	print " date - hence the summation method."


def main(argv):
	SolrStatusFacet.createRRD()
	ss = SolrStatusFacet()
	ss.run()
	ss.createPNG()
	sys.exit(0)

if __name__ == "__main__":
	main(sys.argv[1:])