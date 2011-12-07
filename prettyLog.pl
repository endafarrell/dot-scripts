use strict;
use warnings;

my $LOG_FILE = shift;
open(LOG, $LOG_FILE) || die ("Couldn't open $LOG_FILE - fatal!");
my @logLines = ();
my $longestLine = 0;
while(<LOG>){
	my $currentLine = $_;
	chomp $currentLine;
	$longestLine = (length $currentLine > $longestLine) ? length $currentLine : $longestLine;
	$logLines[@logLines] = $currentLine;
}
close LOG;
my $topRow = "*" x ($longestLine + 4);
my $spf = "%-" . $longestLine . "s"; 
print "$topRow\n";
foreach (@logLines){
		print "* " . sprintf($spf, $_) . " *\n";
}
print "$topRow\n";
