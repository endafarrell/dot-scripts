BEGIN {
        FS="|"
        OFS="|"
        ORS="|\n"
}
{
        four = gensub(".c.", ".L.", "g", $4)
        five = gensub(".cwwtf.", ".lhc.", "g", $5)
        #print $1, $2, $3, $5, $6
        print $2, $3
}

