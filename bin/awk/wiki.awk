# Converts:
#    | 1|http://kv01.back.live.$\{SERVER_DATACENTRE}.local:5984|172.23.c.y1 |kv001.back.live.cwwtf.local:eth0:1|/data/couchdb/1/|
# to:
#    | 1|http://kv01.back.live.$\{SERVER_DATACENTRE}.local:5984|172.23.c.y1 |kv001.back.live.cwwtf.local:eth0:1|172.23.L.y1 |kv001.back.live.lhc.local:eth0:1|/data/couchdb/1/|
BEGIN {
	FS="|"
	OFS="|"
	ORS="|\n"
}
{
	four = gensub(".c.", ".L.", "g", $4)
	five = gensub(".cwwtf.", ".lhc.", "g", $5)
	print $1, $2, $3, $4, $5, four, five, $6
}

