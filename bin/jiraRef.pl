#!/opt/local/bin/perl
$LINE = shift;
my $JIRAREF = "";
if ( $LINE =~ m/(\w+\-\d+)/ ) {
	$JIRAREF = $1;
}
#open (LL, ">>jiraRef.calls");
#print LL "($JIRAREF) $LINE\n";
#close (LL);
print $JIRAREF;
