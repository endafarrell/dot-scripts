import sys # for the command line arg processing
import getopt # for the command line arg processing
import csv

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

sedoc = {}
for k in codes:
	sedoc[codes[k]] = k
	
def main(argv):
	a = sys.argv[1]
	b = sys.argv[2]
	print "a[%s], b[%s]" % (a, b)	
	ar = csv.reader(open(a), delimiter=',', quotechar='"')
	br = csv.reader(open(b), delimiter=',', quotechar='"')
	ab = {}
	for row in ar:
		ab[row[0]] = [row[1],0]
	for row in br:
		if row[0] in ab:
			ab[row[0]] = [ab[row[0]][0],row[1]]
		else:
			ab[row[0]] = [0,row[1]]
	print "country-name,country-3alpha,country-num,%s,%s,delta" % (a,b)
	for row in ab:
		if not row in sedoc:
			continue
		alpha3 = sedoc[row]
		name = names[alpha3]
		print "%s,%s,%s,%s,%s,%s" % (name,alpha3,row, ab[row][0], ab[row][1], int(ab[row][0])-int(ab[row][1]))

if __name__ == "__main__":
	main(sys.argv[1:]) 
