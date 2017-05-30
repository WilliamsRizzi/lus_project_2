#!/usr/bin/env bash

#
# This script is used to train a given CRF++ model using different
# regularization parameters.
#

# check the input parameters, exit if wrong input
if [ "$#" != 1 ]; then 
    echo "Wrong number of parameters."
	echo ""
	echo "Usage: $0 model_number"
    echo ""
    exit 1
fi

# compute the relative path
this=$(dirname $0)

# extract the model to train
model=$1

# try different values for C
cs=(0.5 0.75 1 1.25 1.5 1.75 2 3)
for c in "${cs[@]}"; do
    ${this}/run.sh ${model} ${c} "${model}_${c}"
done
