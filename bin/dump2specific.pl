use strict;
use warnings;
while(<>){
	my $line = $_;
	if ($line =~ /^#/){
		print $line;
	} else {
		my @tabs = split(/	/,$line);
		chomp $tabs[3];
		my @t3colons = split(/:/, $tabs[3]);
		$t3colons[0] =~ s/#//;
		print $tabs[0] . "\t" . $tabs[1] . "\t" . "\$jmx.getAttribute(\"" . $t3colons[0] . ":" . $t3colons[1] . "/" . $t3colons[2] . "\")\t" . $tabs[3] . "\n";
	}
}

