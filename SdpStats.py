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
import sys # for the command line arg processing
#sys.path.append("/home/rouser/enda.farrell/python-libs/")
#import httplib2
#from urllib import urlencode
#import simplejson as json
import getopt # for the command line arg processing
from time import gmtime, strftime
import csv

class SdpStats:
	"""
	  * Generates statistics from the SDP schema
	"""
	countsCsvFile = ""
	alpha3s = ["ABW", "AFG", "AGO", "AIA", "ALA", "ALB", "AND", "ANT", "ARE", \
		"ARG", "ARM", "ASM", "ATA", "ATF", "ATG", "AUS", "AUT", "AZE", "BDI", \
		"BEL", "BEN", "BFA", "BGD", "BGR", "BHR", "BHS", "BIH", "BLM", "BLR", \
		"BLZ", "BMU", "BOL", "BRA", "BRB", "BRN", "BTN", "BVT", "BWA", "CAF", \
		"CAN", "CCK", "CHE", "CHL", "CHN", "CIV", "CMR", "COD", "COG", "COK", \
		"COL", "COM", "CPV", "CRI", "CUB", "CXR", "CYM", "CYP", "CZE", "DEU", \
		"DJI", "DMA", "DNK", "DOM", "DZA", "ECU", "EGY", "ERI", "ESH", "ESP", \
		"EST", "ETH", "FIN", "FJI", "FLK", "FRA", "FRO", "FSM", "FXX", "GAB", \
		"GBR", "GEO", "GGY", "GHA", "GIB", "GIN", "GLP", "GMB", "GNB", "GNQ", \
		"GRC", "GRD", "GRL", "GTM", "GUF", "GUM", "GUY", "HKG", "HMD", "HND", \
		"HRV", "HTI", "HUN", "IDN", "IMN", "IND", "IOT", "IRL", "IRN", "IRQ", \
		"ISL", "ISR", "ITA", "JAM", "JEY", "JOR", "JPN", "KAZ", "KEN", "KGZ", \
		"KHM", "KIR", "KNA", "KOR", "KWT", "LAO", "LBN", "LBR", "LBY", "LCA", \
		"LIE", "LKA", "LSO", "LTU", "LUX", "LVA", "MAC", "MAF", "MAR", "MCO", \
		"MDA", "MDG", "MDV", "MEX", "MHL", "MKD", "MLI", "MLT", "MMR", "MNE", \
		"MNG", "MNP", "MOZ", "MRT", "MSR", "MTQ", "MUS", "MWI", "MYS", "MYT", \
		"NAM", "NCL", "NER", "NFK", "NGA", "NIC", "NIU", "NLD", "NOR", "NPL", \
		"NRU", "NZL", "OMN", "PAK", "PAN", "PCN", "PER", "PHL", "PLW", "PNG", \
		"POL", "PRI", "PRK", "PRT", "PRY", "PSE", "PYF", "QAT", "REU", "ROU", \
		"RUS", "RWA", "SAU", "SCG", "SDN", "SEN", "SGP", "SGS", "SHN", "SJM", \
		"SLB", "SLE", "SLV", "SMR", "SOM", "SPM", "SRB", "STP", "SUR", "SVK", \
		"SVN", "SWE", "SWZ", "SYC", "SYR", "TCA", "TCD", "TGO", "THA", "TJK", \
		"TKL", "TKM", "TLS", "TON", "TTO", "TUN", "TUR", "TUV", "TWN", "TZA", \
		"UGA", "UKR", "UMI", "URY", "USA", "UZB", "VAT", "VCT", "VEN", "VGB", \
		"VIR", "VNM", "VUT", "WLF", "WSM", "YEM", "ZAF", "ZMB", "ZWE"]
	names = {
		"ALA":"Aaland Islands",
		"AFG":"Afghanistan",
		"ALB":"Albania",
		"DZA":"Algeria",
		"ASM":"American Samoa",
		"AND":"Andorra",
		"AGO":"Angola",
		"AIA":"Anguilla",
		"ATA":"Antarctica",
		"ATG":"Antigua and Barbuda",
		"ARG":"Argentina",
		"ARM":"Armenia",
		"ABW":"Aruba",
		"AUS":"Australia",
		"AUT":"Austria",
		"AZE":"Azerbaijan",
		"BHS":"The Bahamas",
		"BHR":"Bahrain",
		"BGD":"Bangladesh",
		"BRB":"Barbados",
		"BLR":"Belarus",
		"BEL":"Belgium",
		"BLZ":"Belize",
		"BEN":"Benin",
		"BMU":"Bermuda",
		"BTN":"Bhutan",
		"BOL":"Bolivia",
		"BIH":"Bosnia and Herzegovina",
		"BWA":"Botswana",
		"BVT":"Bouvet Island",
		"BRA":"Brazil",
		"IOT":"British Indian Ocean Territory",
		"VGB":"British Virgin Islands",
		"BRN":"Brunei",
		"BGR":"Bulgaria",
		"BFA":"Burkina Faso",
		"MMR":"Burma",
		"BDI":"Burundi",
		"KHM":"Cambodia",
		"CMR":"Cameroon",
		"CAN":"Canada",
		"CPV":"Cape Verde",
		"CYM":"Cayman Islands",
		"CAF":"Central African Republic",
		"TCD":"Chad",
		"CHL":"Chile",
		"CHN":"China",
		"CXR":"Christmas Island",
		"CCK":"Cocos (Keeling) Islands",
		"COL":"Colombia",
		"COM":"Comoros",
		"COD":"Democratic Republic of the Congo",
		"COG":"Republic of the Congo",
		"COK":"Cook Islands",
		"CRI":"Costa Rica",
		"CIV":"Cote d'Ivoire",
		"HRV":"Croatia",
		"CUB":"Cuba",
		"CYP":"Cyprus",
		"CZE":"Czech Republic",
		"DNK":"Denmark",
		"DJI":"Djibouti",
		"DMA":"Dominica",
		"DOM":"Dominican Republic",
		"ECU":"Ecuador",
		"EGY":"Egypt",
		"SLV":"El Salvador",
		"GNQ":"Equatorial Guinea",
		"ERI":"Eritrea",
		"EST":"Estonia",
		"ETH":"Ethiopia",
		"FLK":"Falkland Islands (Islas Malvinas)",
		"FRO":"Faroe Islands",
		"FJI":"Fiji",
		"FIN":"Finland",
		"FRA":"France",
		"FXX":"Metropolitan France",
		"GUF":"French Guiana",
		"PYF":"French Polynesia",
		"ATF":"French Southern and Antarctic Lands",
		"GAB":"Gabon",
		"GMB":"The Gambia",
		"PSE":"Palestine (West Bank, Gaza Strip)",
		"GEO":"Georgia",
		"DEU":"Germany",
		"GHA":"Ghana",
		"GIB":"Gibraltar",
		"GRC":"Greece",
		"GRL":"Greenland",
		"GRD":"Grenada",
		"GLP":"Guadeloupe",
		"GUM":"Guam",
		"GTM":"Guatemala",
		"GGY":"Guernsey",
		"GIN":"Guinea",
		"GNB":"Guinea-Bissau",
		"GUY":"Guyana",
		"HTI":"Haiti",
		"HMD":"Heard Island and McDonald Islands",
		"VAT":"Holy See (Vatican City)",
		"HND":"Honduras",
		"HKG":"Hong Kong",
		"HUN":"Hungary",
		"ISL":"Iceland",
		"IND":"India",
		"IDN":"Indonesia",
		"IRN":"Iran",
		"IRQ":"Iraq",
		"IRL":"Ireland",
		"IMN":"Isle of Man",
		"ISR":"Israel",
		"ITA":"Italy",
		"JAM":"Jamaica",
		"JPN":"Japan",
		"JEY":"Jersey",
		"JOR":"Jordan",
		"KAZ":"Kazakhstan",
		"KEN":"Kenya",
		"KIR":"Kiribati",
		"PRK":"North Korea",
		"KOR":"South Korea",
		"KWT":"Kuwait",
		"KGZ":"Kyrgyzstan",
		"LAO":"Laos",
		"LVA":"Latvia",
		"LBN":"Lebanon",
		"LSO":"Lesotho",
		"LBR":"Liberia",
		"LBY":"Libya",
		"LIE":"Liechtenstein",
		"LTU":"Lithuania",
		"LUX":"Luxembourg",
		"MAC":"Macau",
		"MKD":"Macedonia",
		"MDG":"Madagascar",
		"MWI":"Malawi",
		"MYS":"Malaysia",
		"MDV":"Maldives",
		"MLI":"Mali",
		"MLT":"Malta",
		"MHL":"Marshall Islands",
		"MTQ":"Martinique",
		"MRT":"Mauritania",
		"MUS":"Mauritius",
		"MYT":"Mayotte",
		"MEX":"Mexico",
		"FSM":"Federated States of Micronesia",
		"MDA":"Moldova",
		"MCO":"Monaco",
		"MNG":"Mongolia",
		"MNE":"Montenegro",
		"MSR":"Montserrat",
		"MAR":"Morocco",
		"MOZ":"Mozambique",
		"NAM":"Namibia",
		"NRU":"Nauru",
		"NPL":"Nepal",
		"NLD":"Netherlands",
		"ANT":"Netherlands Antilles",
		"NCL":"New Caledonia",
		"NZL":"New Zealand",
		"NIC":"Nicaragua",
		"NER":"Niger",
		"NGA":"Nigeria",
		"NIU":"Niue",
		"NFK":"Norfolk Island",
		"MNP":"Northern Mariana Islands",
		"NOR":"Norway",
		"OMN":"Oman",
		"PAK":"Pakistan",
		"PLW":"Palau",
		"PAN":"Panama",
		"PNG":"Papua New Guinea",
		"PRY":"Paraguay",
		"PER":"Peru",
		"PHL":"Philippines",
		"PCN":"Pitcairn Islands",
		"POL":"Poland",
		"PRT":"Portugal",
		"PRI":"Puerto Rico",
		"QAT":"Qatar",
		"REU":"Reunion",
		"ROU":"Romania",
		"RUS":"Russia",
		"RWA":"Rwanda",
		"BLM":"Saint Barthelemy",
		"SHN":"Saint Helena",
		"KNA":"Saint Kitts and Nevis",
		"LCA":"Saint Lucia",
		"MAF":"Saint Martin",
		"SPM":"Saint Pierre and Miquelon",
		"VCT":"Saint Vincent and the Grenadines",
		"WSM":"Samoa",
		"SMR":"San Marino",
		"STP":"Sao Tome and Principe",
		"SAU":"Saudi Arabia",
		"SEN":"Senegal",
		"SCG":"Serbia and Montenegro",
		"SRB":"Serbia",
		"SYC":"Seychelles",
		"SLE":"Sierra Leone",
		"SGP":"Singapore",
		"SVK":"Slovakia",
		"SVN":"Slovenia",
		"SLB":"Solomon Islands",
		"SOM":"Somalia",
		"ZAF":"South Africa",
		"SGS":"South Georgia and the Islands",
		"ESP":"Spain",
		"LKA":"Sri Lanka",
		"SDN":"Sudan",
		"SUR":"Suriname",
		"SJM":"Svalbard",
		"SWZ":"Swaziland",
		"SWE":"Sweden",
		"CHE":"Switzerland",
		"SYR":"Syria",
		"TWN":"Taiwan",
		"TJK":"Tajikistan",
		"TZA":"Tanzania",
		"THA":"Thailand",
		"TLS":"Timor-Leste",
		"TGO":"Togo",
		"TKL":"Tokelau",
		"TON":"Tonga",
		"TTO":"Trinidad and Tobago",
		"TUN":"Tunisia",
		"TUR":"Turkey",
		"TKM":"Turkmenistan",
		"TCA":"Turks and Caicos Islands",
		"TUV":"Tuvalu",
		"UGA":"Uganda",
		"UKR":"Ukraine",
		"ARE":"United Arab Emirates",
		"GBR":"United Kingdom",
		"USA":"United States",
		"UMI":"United States Minor Outlying Islands",
		"URY":"Uruguay",
		"UZB":"Uzbekistan",
		"VUT":"Vanuatu",
		"VEN":"Venezuela",
		"VNM":"Vietnam",
		"VIR":"Virgin Islands",
		"WLF":"Wallis and Futuna",
		"ESH":"Western Sahara",
		"YEM":"Yemen",
		"ZMB":"Zambia",
		"ZWE":"Zimbabwe"
	}
	providers = [ \
		"adplaces", \
		"afisha", \
		"alwadha", \
		"apontador", \
		"bookatable", \
		"bookmyshow", \
		"burrp", \
		"cartrawler", \
		"cityvox", \
		"coigdzie", \
		"ctrip", \
		"Enda", \
		"esthu", \
		"expedia", \
		"explorer", \
		"fantong", \
		"funguide", \
		"ganji", \
		"ganji-neighbourhood", \
		"gary", \
		"gaultmillau", \
		"green-explorer", \
		"hrs", \
		"hungrygw", \
		"ics_alwadha", \
		"ics_alwadha_egy", \
		"ics_dgs", \
		"ics_goldenpages", \
		"ics_midland", \
		"ics_truovo_bel", \
		"ics_truovo_irl", \
		"ics_truovo_prt", \
		"ics_yell", \
		"iinfoest", \
		"iinfolat", \
		"iinfolet", \
		"ijazza", \
		"interinfo", \
		"jiepang", \
		"khalabi", \
		"langenscheidt", \
		"lcms", \
		"lcms-el", \
		"lokaldelen", \
		"lonely", \
		"Lothar Schulz", \
		"macmahon", \
		"map-area",
		"map-landmark", \
		"michelin", \
		"midland", \
		"mountain", \
		"navteq", \
		"navteq-china", \
		"navteq-el", \
		"navteq-el-china-A", \
		"navteq-el-china-B", \
		"navteq-el-china-C", \
		"navteq-indoor-maps", \
		"navteq_lpa", \
		"nokia", \
		"nokia-china", \
		"nokia-search", \
		"nokia-shops-turkey", \
		"opr-auto-merge", \
		"opr-editorial", \
		"opr-editorial-bad-utf8", \
		"opr-quality", \
		"opr-test-community", \
		"opr-test-trusted", \
		"orange_cityvox", \
		"orange_mpl", \
		"orange_mpl_ad", \
		"ovi", \
		"ovi-checkin", \
		"piao", \
		"place-matching-check", \
		"pnss", \
		"primeplaces", \
		"primeplaces-editorial", \
		"protected", \
		"publictransport", \
		"qunar", \
		"qype", \
		"radar", \
		"safarinow", \
		"sanoma", \
		"semaloc", \
		"semaloc-digu", \
		"semaloc-facebook", \
		"semaloc-foursquare", \
		"semaloc-gowalla", \
		"semaloc-jiepang", \
		"semaloc-other", \
		"semaloc-qype", \
		"semaloc-sohu", \
		"sohuauto", \
		"soufun", \
		"telefoongids", \
		"telegate", \
		"telelistas", \
		"theaa", \
		"timeout", \
		"tracks4africa", \
		"travelguru", \
		"tripadvisor", \
		"vodafonehu", \
		"wcities", \
		"wcities_events", \
		"wcities_movies", \
		"weekendhk", \
		"yell", \
		"zhaopin", \
		"ziva" \
	]
	
	codes = {
		"ALA":"248",
		"AFG":"004",
		"ALB":"008",
		"DZA":"012",
		"ASM":"016",
		"AND":"020",
		"AGO":"024",
		"AIA":"660",
		"ATA":"010",
		"ATG":"028",
		"ARG":"032",
		"ARM":"051",
		"ABW":"533",
		"AUS":"036",
		"AUT":"040",
		"AZE":"031",
		"BHS":"044",
		"BHR":"048",
		"BGD":"050",
		"BRB":"052",
		"BLR":"112",
		"BEL":"056",
		"BLZ":"084",
		"BEN":"204",
		"BMU":"060",
		"BTN":"064",
		"BOL":"068",
		"BIH":"070",
		"BWA":"072",
		"BVT":"074",
		"BRA":"076",
		"IOT":"086",
		"VGB":"092",
		"BRN":"096",
		"BGR":"100",
		"BFA":"854",
		"MMR":"104",
		"BDI":"108",
		"KHM":"116",
		"CMR":"120",
		"CAN":"124",
		"CPV":"132",
		"CYM":"136",
		"CAF":"140",
		"TCD":"148",
		"CHL":"152",
		"CHN":"156",
		"CXR":"162",
		"CCK":"166",
		"COL":"170",
		"COM":"174",
		"COD":"180",
		"COG":"178",
		"COK":"184",
		"CRI":"188",
		"CIV":"384",
		"HRV":"191",
		"CUB":"192",
		"CYP":"196",
		"CZE":"203",
		"DNK":"208",
		"DJI":"262",
		"DMA":"212",
		"DOM":"214",
		"ECU":"218",
		"EGY":"818",
		"SLV":"222",
		"GNQ":"226",
		"ERI":"232",
		"EST":"233",
		"ETH":"231",
		"FLK":"238",
		"FRO":"234",
		"FJI":"242",
		"FIN":"246",
		"FRA":"250",
		"FXX":"249",
		"GUF":"254",
		"PYF":"258",
		"ATF":"260",
		"GAB":"266",
		"GMB":"270",
		"PSE":"275",
		"GEO":"268",
		"DEU":"276",
		"GHA":"288",
		"GIB":"292",
		"GRC":"300",
		"GRL":"304",
		"GRD":"308",
		"GLP":"312",
		"GUM":"316",
		"GTM":"320",
		"GGY":"831",
		"GIN":"324",
		"GNB":"624",
		"GUY":"328",
		"HTI":"332",
		"HMD":"334",
		"VAT":"336",
		"HND":"340",
		"HKG":"344",
		"HUN":"348",
		"ISL":"352",
		"IND":"356",
		"IDN":"360",
		"IRN":"364",
		"IRQ":"368",
		"IRL":"372",
		"IMN":"833",
		"ISR":"376",
		"ITA":"380",
		"JAM":"388",
		"JPN":"392",
		"JEY":"832",
		"JOR":"400",
		"KAZ":"398",
		"KEN":"404",
		"KIR":"296",
		"PRK":"408",
		"KOR":"410",
		"KWT":"414",
		"KGZ":"417",
		"LAO":"418",
		"LVA":"428",
		"LBN":"422",
		"LSO":"426",
		"LBR":"430",
		"LBY":"434",
		"LIE":"438",
		"LTU":"440",
		"LUX":"442",
		"MAC":"446",
		"MKD":"807",
		"MDG":"450",
		"MWI":"454",
		"MYS":"458",
		"MDV":"462",
		"MLI":"466",
		"MLT":"470",
		"MHL":"584",
		"MTQ":"474",
		"MRT":"478",
		"MUS":"480",
		"MYT":"175",
		"MEX":"484",
		"FSM":"583",
		"MDA":"498",
		"MCO":"492",
		"MNG":"496",
		"MNE":"499",
		"MSR":"500",
		"MAR":"504",
		"MOZ":"508",
		"NAM":"516",
		"NRU":"520",
		"NPL":"524",
		"NLD":"528",
		"ANT":"530",
		"NCL":"540",
		"NZL":"554",
		"NIC":"558",
		"NER":"562",
		"NGA":"566",
		"NIU":"570",
		"NFK":"574",
		"MNP":"580",
		"NOR":"578",
		"OMN":"512",
		"PAK":"586",
		"PLW":"585",
		"PAN":"591",
		"PNG":"598",
		"PRY":"600",
		"PER":"604",
		"PHL":"608",
		"PCN":"612",
		"POL":"616",
		"PRT":"620",
		"PRI":"630",
		"QAT":"634",
		"REU":"638",
		"ROU":"642",
		"RUS":"643",
		"RWA":"646",
		"BLM":"652",
		"SHN":"654",
		"KNA":"659",
		"LCA":"662",
		"MAF":"663",
		"SPM":"666",
		"VCT":"670",
		"WSM":"882",
		"SMR":"674",
		"STP":"678",
		"SAU":"682",
		"SEN":"686",
		"SCG":"891",
		"SRB":"688",
		"SYC":"690",
		"SLE":"694",
		"SGP":"702",
		"SVK":"703",
		"SVN":"705",
		"SLB":"090",
		"SOM":"706",
		"ZAF":"710",
		"SGS":"239",
		"ESP":"724",
		"LKA":"144",
		"SDN":"736",
		"SUR":"740",
		"SJM":"744",
		"SWZ":"748",
		"SWE":"752",
		"CHE":"756",
		"SYR":"760",
		"TWN":"158",
		"TJK":"762",
		"TZA":"834",
		"THA":"764",
		"TLS":"626",
		"TGO":"768",
		"TKL":"772",
		"TON":"776",
		"TTO":"780",
		"TUN":"788",
		"TUR":"792",
		"TKM":"795",
		"TCA":"796",
		"TUV":"798",
		"UGA":"800",
		"UKR":"804",
		"ARE":"784",
		"GBR":"826",
		"USA":"840",
		"UMI":"581",
		"URY":"858",
		"UZB":"860",
		"VUT":"548",
		"VEN":"862",
		"VNM":"704",
		"VIR":"850",
		"WLF":"876",
		"ESH":"732",
		"YEM":"887",
		"ZMB":"894",
		"ZWE":"716"
	}
	def __init__(self, countsCsvFile):
		self.countsCsvFile = countsCsvFile
	
	def __str__( self ) :
		return "SdpStats counts[%s]" % self.countsCsvFile
	
	def run(self):
		""" Iterates over the countries """
		reader = csv.reader( open(self.countsCsvFile), delimiter=',', quotechar='"')
		codeCount = {}
		for row in reader:
			codeCount[row[0]] = int(row[1])
		print "<div><table>"
		print "<tr><th>country</th><th>code</th><th>SDP</th></tr>"
		for alpha3 in self.alpha3s:
			code = self.codes[alpha3]
			if code in codeCount:
				counts = codeCount[code]
			else:
				counts = 0
			print "<tr><td>%s</td><td>%s</td><td>%d</td></tr>" \
					% (self.names[alpha3], alpha3, counts)
		utc = strftime("%Y-%m-%d %H:%M:%S UTC", gmtime())
		print "</table>Data as of %s</div>" % utc
	
	def providerStats(self):
		""" Iterates over the countries and providers!"""
		print "<div><table>"
		print "<tr><th>country</th>",
		for provider in self.providers:
			print "<th>%s</th>" % provider,
		print "</tr>"
		for alpha3 in self.alpha3s:
			print "<tr><td>%s</td>" % self.names[alpha3],
			for provider in self.providers:
				active = self.countryProviderActive(alpha3, provider)
				print "<td>%s</td>" % str(active), 
			print "</tr>"
		utc = strftime("%Y-%m-%d %H:%M:%S UTC", gmtime())
		print "</table>Data as of %s</div>" % utc
	
	def countryStatusCounts(self, alpha3):
		""" Returns a list containing the Solr count of (in the order
		specified in self.statuses) each status for the alpha3 country """
		counts = []
		for i in range(3):
			status = self.statuses[i]
			query = "countrycode:\"%s\" AND status:%s" % (alpha3, status)
			params = urlencode({"q":query, "start":0, "rows":0})
			url = "%s/select?%s" % (self.solrBaseUrl, params)
			resp, content = self._GetCommands(url, True)
			counts.append(self.extractCount(content))
		return counts

	def countryProviderActive(self, alpha3, provider):
		query = "countrycode:\"%s\" AND status:ACTIVE AND managedby:%s" % (alpha3, provider)
		params = urlencode({"q":query, "start":0, "rows":0})
		url = "%s/select?%s" % (self.solrBaseUrl, params)
		resp, content = self._GetCommands(url, True)
		return self.extractCount(content)
	
	def extractCount(self, content):
		tree = ET.XML(content)
		result = (tree.findall(".//result"))[0]
		return int(result.attrib.get("numFound"))

		
	def _GetCommands(self, url, extraSolrProcessing=False):
		""" There be dragons here! This method may throw exceptions and
		depending on where in the process it may leave the backup (or
		restore) server in an unusable state! """
		# try:
		# 	# Don't reuse these
		# 	h = httplib2.Http(".cache")
		# 	resp, content = h.request(url, "GET")
		# except AttributeError:
		# 	msg = "GET on '%s' raised an \"AttrbuteError\" which" % url
		# 	msg = "%s mostly means that the server is not accessible" % msg
		# 	raise Exception(msg)
		# if not (resp['status'] == '200' or resp['status'] == '304'):
		# 	raise Exception("GET on %s returned a status of %s\n%s\n%s" \
		# 		% (url, resp['status'], resp, content))
		resp, content = self._doHttp("GET", url, ['200', '304'])
		if extraSolrProcessing:
			# You're gonna love this next part. Solr can, and does, at least
			# as of 1.4.x, return a 200 status when the content shows an
			# exception (which can also be seen in the logs). So, we need to
			# find these and not ignore their presence.
			tree = ET.XML(content)
			strs = tree.findall(".//str")
			for s in strs:
				if "exception" == s.attrib.get("name"):
					raise Exception("GET on %s returned a status of %s\n%s\n%s" \
						% (url, resp['status'], resp, content))
		return resp, content
	
	def _doHttp(self, method, url, okResponses, body="", headers={}):
		""" There be dragons here! This may throw exceptions! """
		method = method.upper()
		try:
			#h = httplib2.Http(".cache")
			h = httplib2.Http()
			if method in ['POST', 'PUT']:
				resp, content = h.request(url, method, body=body, headers=headers)
			else:
				resp, content = h.request(url, method)
		except AttributeError, e:
			print "*****"
			print e
			print "*****"
			msg = "%s on '%s' raised and \"AttributeError\" which" % (method, url)
			msg = "%s mostly means that the server is not accessible" % msg
			raise Exception(msg)
		if not resp['status'] in okResponses:
			raise Exception("%s on %s returned a status of %s\n%s\n%s" \
				% (method, url, resp['status'], resp, content))
		return resp, content


def usage():
	print "Usage: python SolrStats.py"
	print " --help              get this help/usage message"
	print " --solrBaseUrl <url> set the Solr service & core endpoint. The"
	print "                        queries are sent to that core."
	print " --as-html           print as HTML instead of as a CSV"


def main(argv):
	
	solrBaseUrl = ""
	asHTML = False
	providers = False
	try:
		opts, args = getopt.getopt(argv, "", ["help", "solrBaseUrl=", "as-html", "providers"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-s", "--solrBaseUrl"):
			solrBaseUrl = arg
		elif opt in ("-a", "--as-html"):
			asHTML = True
		elif opt == "--providers":
			providers = True

	if solrBaseUrl == "":
		usage()
		print "Specify --solrBaseUrl!"
		print argv
		#sys.exit(2)
	ss = SdpStats("./sample.csv")
	ss.run()
	sys.exit(0)

if __name__ == "__main__":
	main(sys.argv[1:]) 
