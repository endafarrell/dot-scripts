#!/usr/bin/perl -w

# geohash_sample.pl - use KML to display points and bounding boxes 
# for one point as you drop the number of digits in the Geo Hash
# (http://geohash.com) representation of that point.
#
# I've been exploring using geohashes as a way of dropping precision
# for privacy protection from coordinates.  I wanted to visualize
# what would happen as I dropped digits of precision.
# 
# usage:
# ./geohash_geohash_to_kml.pl geohash > foo.kml

# Written by Rich Gibson, and released into the public domain.
# see mappinghacks.com

use strict;
use Data::Dumper;
use Geo::Hash;
my $gh = new Geo::Hash;
my $h = $ARGV[0]; 

print kml_header('geohash data');

foreach my $i (0..length($h)-1) {
    my $hsmall = substr($h, 0, length($h) -$i);
    my ($latrange, $lngrange) = $gh->decode_to_interval($hsmall);
    my ($lat, $lng) = $gh->decode($hsmall);

    # calculate distance between the corners of the bounding box.
    my $d1 = dist($latrange->[0],$lngrange->[0], $latrange->[1], $lngrange->[0]);
    
    $d1 = sprintf("%5.7f", $d1);
    if ($d1 < 1) {
        $d1 = ($d1 * 5280) . " feet";
    } else {
        $d1 = $d1 . " miles";
    }

    # prints lat/lng ranges
    #warn "($latrange->[0],$lngrange->[0]), ($latrange->[1], $lngrange->[0])\t = $d1\n";
    my $t = "\t" x (1 - ( int(length($hsmall)/8)) );
    #warn  "$hsmall\t$t center ($lat, $lng) bbox diagonal distance= $d1\n";
    print polygon("level $i $hsmall bbox", $latrange->[0],$lngrange->[0], $latrange->[1], $lngrange->[1]);
    print qq(    <Placemark>
      <name>$hsmall</name>
      <description><![CDATA[ $i $hsmall<br /> $lat, $lng ]]></description>
      <styleUrl>#foo</styleUrl>
      <Point>
        <coordinates>$lng,$lat,0</coordinates>
      </Point>
    </Placemark>
);


}


print kml_footer();

sub polygon {
    my ($name, $lat1, $lng1, $lat2, $lng2) = @_;
    return qq(    <Placemark>
        <name>$name</name>
        <styleUrl>#PolyStyle</styleUrl>
        <Polygon>
            <tessellate>1</tessellate>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>
                      $lng1,$lat1,0
                      $lng2,$lat1,0
                      $lng2,$lat2,0
                      $lng1,$lat2,0
                      $lng1,$lat1,0
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
);

}
sub dist {
    # allow dist to be called as either $self->dist() or dist()
    my @parms = @_;

    my $pi = atan2(1,1) * 4;
    my $lat1 = $parms[0]/180 * $pi ;
    my $long1 = $parms[1]/180 * $pi;
    my $lat2 = $parms[2]/180 * $pi;
    my $long2 = $parms[3]/180 * $pi;

    $a = $long1 - $long2;
    if ($a < 0) {$a = -$a;}
    if ($a > $pi) {$a = 2 * $pi;}
    my $dist;
    eval {
      $dist = acos(sin($lat2) * sin($lat1) + cos($lat2)*cos($lat1)*cos($a)) * 3958;
    };
    return ($dist);
}
sub acos {
    atan2( sqrt(1-$_[0] * $_[0]), $_[0])
}


sub kml_header {
    my ($folder_name) = @_;
    return qq(<?xml version="1.0" encoding="UTF-8"?>
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
    </Style>
);
}
sub kml_footer {
    return qq(
  </Document>
</kml>
)
}
