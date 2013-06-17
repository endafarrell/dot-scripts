#!/usr/bin/perl -w
use warnings;
use strict;

use Scalar::Util qw(looks_like_number);

my $sum = 0;
my $count = 0;
my $fail = 0;
my $pass = 0;
while (<>) {
    chomp;
    $count++;
    my $current_value = $_; #assume input is 1 value/line for simplicity sake
    if (looks_like_number($current_value)){
        $sum += $current_value;
        if ($current_value > 25) {
            $fail++;
        } else {
            $pass++;
        }
    }
}
my $mean = $sum / $count;
my $passPct = 100 * $pass / $count;
my $failPct = 100 * $fail / $count;
printf("count: %d mean: %5.3f pass: %5.3f%% fail: %5.3f%% (pass/fail wrt 25)\n", $count, $mean, $passPct, $failPct);
