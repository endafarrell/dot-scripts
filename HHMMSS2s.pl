#!/usr/bin/perl

while(<>){
	my ($tm, $dat) = split(',');
	my ($h, $m, $s) = split(':', $tm);
	my $S = ($h * 60 * 60 + $m * 60 + $s);
	print "S[$S], tm[$tm], h[$h], m[$m], s[$s], dat=$dat"
}
