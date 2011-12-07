for H in 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    for M1 in 0 1 2 3 4 5; do
        for M2 in 0 1 2 3 4 5 6 7 8 9; do
            tm="$H:$M1$M2"
            s=$(grep $tm $1 | cut -f2 -d',')
            if [ "x$s" == "x" ]; then
                s=0
            fi
            f=$(grep $tm $2 | cut -f2 -d',')
            if [ "x$f" == "x" ]; then
                f=0
            fi
            echo "$H:$M1$M2,$s,$f"
        done
    done         
done
