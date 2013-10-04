#!/bin/bash
for i in `seq 100`; do
    if [[ $i == $1 ]]; then sleep 1; fi
    sleep 0.01
    echo $i
done
