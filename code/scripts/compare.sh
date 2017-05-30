#!/usr/bin/env bash

#
# This script is used to compare the performances of
# all models trained so far.
#

# extract the model name from the file path
function parse_model() {
    cat - | sed 's/computations\/\(.*\)\/performances$/\1/'
}

# parse the output of the evaluation script
function parse_performances() {
    cat - | sed -n 2p | sed 's/^.*precision: *\(.*\)%; recall: *\(.*\)%; FB1: *\(.*\)$/\1% \2% \3%/'
}

# comparison
for file in "computations/*/*/performances"; do
    model=$(echo $file)
    for m in $model; do
        echo -n $m | parse_model
        echo -n ' '
        cat $m | parse_performances
    done
done
