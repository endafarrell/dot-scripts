#!/bin/bash
IFS='!'

function createImage() {
    args=("$@")
    image=${args[1]}
    start=${args[2]}
    echo ${args[1]}
    end=${args[3]}
    title=${args[4]}
    vlabel=${args[5]}
    graph=${args[6]}
    
    start=$(echo $start | sed 's/now/1304690400/')
    end=$(echo $end | sed 's/now/1304690400/')
    
    echo "rrdtool graph $image STD_SETTINGS --start $start --end $end \
        --title $title --vertical-label $vlabel \
        $graph 1>/dev/null"

}

createImage "enda.jpg!now-1d!now"
