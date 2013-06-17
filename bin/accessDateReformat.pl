#!/usr/bin/perl
use POSIX;
use strict;
my %months = (
    "Jan" => "01",
    "Feb" => "02",
    "Mar" => "03",
    "Apr" => "04",
    "May" => "05",
    "Jun" => "06",
    "Jul" => "07",
    "Aug" => "08",
    "Sep" => "09",
    "Oct" => "10",
    "Nov" => "11",
    "Dec" => "12"
);

while (<STDIN>) {
	# The line will look like this:
	# 94.198.60.5 - - [05/Oct/2011:08:26:25 +0000] "POST url" 200 - 232
	my @words = split(' ', $_, 5);
	my $a = $words[0];
	my $b = $words[1];
	my $c = $words[2];
	my ($D, $H, $M, $S) = split(':', $words[3]);
	my ($day, $MON, $y) = split('/', $D);
	$day = substr($day, 1);
	my $d = $words[4];

	my $month = $months{$MON};
	
	print "$a $b $c $y/$month/$day\T$H$M$S $d";
}

