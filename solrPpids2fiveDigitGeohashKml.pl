#!/usr/bin/perl -w

use Data::Dumper;
use Geo::Hash;
my $gh = new Geo::Hash;
### 5, the default, is a smallish, "district" sized area.
### 4 is town/small city sized,
### 3 is 100sq km and good if you want to create a KML covering
###   the entire planet
my $KML_GEOHASH_LEN =  $ENV{'KML_GEOHASH_LEN'} || 5; 
my %uniqueGeohashs = ();

while (<>) {
  chomp;
  my $geoH = substr($_, 0, $KML_GEOHASH_LEN); 
  if ( exists $uniqueGeohashs{$geoH} ){
    $uniqueGeohashs{$geoH} = $uniqueGeohashs{$geoH} + 1;
  } else {
    $uniqueGeohashs{$geoH} = 1;
  };
  # Poor-man's memory/bug limitation
  if ( scalar keys ( %uniqueGeohashs ) > 5000000 ){
    die "The number of distinct geo hashs is too large!";
  }
}
my $numUniqueGeohashs = scalar keys ( %uniqueGeohashs );
print kml_header("Shows $numUniqueGeohashs $KML_GEOHASH_LEN-digit geohashs and the count of places therein");
for my $geoHash ( sort keys %uniqueGeohashs ){
  my $num = $uniqueGeohashs{$geoHash};
  eval {
    my ($latrange, $lngrange) = $gh->decode_to_interval($geoHash);
    my ($lat, $lng) = $gh->decode($geoHash);
    print polygon("$geoHash: $num", $lat, $lng, $latrange->[0], $lngrange->[0], $latrange->[1], $lngrange->[1], $num);
  }
} 
print kml_footer();


# Add just above the polygon line:
#          <Point> <coordinates>$lng, $lat, $altitude</coordinates> </Point>
sub polygon {
  my ($name, $lat, $lng, $lat1, $lng1, $lat2, $lng2, $num) = @_;
  my $altitude = 3 * $num * (10 ** ($KML_GEOHASH_LEN - 3));
  return qq(
    <Placemark>
      <name>$name</name>
      <styleUrl>#PolyStyle</styleUrl>
      <Polygon>
        <extrude>1</extrude>
        <altitudeMode>relativeToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
             $lng1,$lat1,$altitude
             $lng2,$lat1,$altitude
             $lng2,$lat2,$altitude
             $lng1,$lat2,$altitude
             $lng1,$lat1,$altitude
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>);

}


sub kml_header {
    my ($folder_name) = @_;
    return qq(<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Style id="PolyStyle">
      <PolyStyle>
        <color>33000000</color><!-- aabbggrr -->
        <colorMode>random</colorMode>
        <fill>1</fill>
      </PolyStyle>
      <IconStyle id="ID">
        <color>ffffffff</color>
        <colorMode>normal</colorMode>
        <scale>0</scale>
        <heading>0</heading>
        <Icon>
          <href>...</href>
        </Icon>
        <hotSpot x="0.5"  y="0.5" xunits="fraction" yunits="fraction"/>
      </IconStyle>
    </Style>
    <name>Nokia Places Registry geospacial coverage</name>
    <Folder>
      <name>$folder_name</name>
      <open>1</open>
);
}
sub kml_footer {
    return qq(
    </Folder>
  </Document>
</kml>
)
}
