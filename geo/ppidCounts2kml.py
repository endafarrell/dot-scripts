#!/usr/bin/python
# -*- coding: utf-8 -*-
import geohash
import sys
import json
import requests

class PpidCounts2KML:
  URL = "http://api.places.maps.ovi.com/rest/v1/places/%s"
  PROXY = {"http" :  "http://nokes.nokia.com:8080"}
  TIMEOUT = 1.1

  def __init__(self, filename):
    self.csvs = open(filename,"r").readlines()
    self.geohashCount = {}

  def run(self):
    #print self.csvs
    #print geohash.decode("u27")
    #print geohash.bbox("u27")
    i = 0
    for csv in self.csvs:
      i += 1
      place = self.processPlace(csv, i)
      self.csvs[i - 1] = place
      if i == 1001:
        self.csvs = self.csvs[:i]
        break
    self.dump()

  def processPlace(self, csv, index):
    (ppid, count) = csv.split(",")
    count = long(count)
    gh = ppid[3:8]
    self.updateGeohashCount(gh, count)
    url = self.URL % ppid
    try:
      resp = requests.get(url=url, proxies=self.PROXY, timeout=self.TIMEOUT)
    except requests.exceptions.RequestException:
      # Timeouts are the most likely problem here, but for this we can skip
      return None
    data = json.loads(resp.content)
    # The JSON has a root node called "place" in which everything is found
    if "place" not in data:
      # When the response does not contain a "place" object, there is little
      # we can do
      return None
    data = data["place"]
    name = data["names"]["defaultName"]["name"]
    lat = data["location"]["geoCoordinates"]["latitude"]
    lng = data["location"]["geoCoordinates"]["longitude"]
    return { "ppid": ppid,
             "name": "#%d (%d views): %s" % (index, count, name.replace("&", "&amp;")), 
             "count": count, 
             "lat": lat, 
             "lng": lng, 
             "geohash":gh }
    
  def updateGeohashCount(self, gh, count):
    if gh in self.geohashCount:
      self.geohashCount[gh] = self.geohashCount[gh] + count
    else:
      self.geohashCount[gh] = count


  def dump(self):
    print """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
  <Document 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://earth.google.com/kml/2.1
    http://code.google.com/apis/kml/schema/kml21.xsd">
    <Style id="PolyStyle">
      <PolyStyle>
        <color>77000000</color>
        <colorMode>random</colorMode>
        <fill>1</fill>
      </PolyStyle>
    </Style>"""
    for place in self.csvs:
      self.dumpPlace(place)
    print """  </Document>
</kml>"""
    
  def dumpPlace(self, place):
    if place is None:
      return
    placemark = """    <Placemark>
      <name>%s</name>
      <description><![CDATA[<div id="basicPlaceContainer" style="width:620px; height:350px;"></div>
<script src="http://api.maps.nokia.com/places/beta2/jsPlacesAPI.js"></script>
<script>
  var basicPlace = new nokia.places.Place({
      placeId: '%s',
      targetNode: 'basicPlaceContainer',
      template: 'nokia.blue.place'
  });
</script>]]></description>
      <Point>
        <coordinates>%s,%s</coordinates>
      </Point>
    </Placemark>""" % (place["name"], place["ppid"], place["lng"], place["lat"])
    print placemark.encode("utf-8")

def main(argv):
  x = PpidCounts2KML(argv[0])
  x.run()

if __name__ == "__main__":
  main(sys.argv[1:])
