#!/usr/bin/env bash

#
# This script is used to train a given CRF++ model and evaluate its performances.
#

# compute the relative path
this=$(dirname $0)

# check the input parameters, exit if wrong input
if [ "$#" != 1 ] && [ "$#" != 3 ]; then 
    echo "Wrong number of parameters."
	echo ""
	echo "Usage: $0 model_number [regularization_value target_output]"
    echo ""
    exit 1
fi

# extract the model to train and the value for c
model=$1
c=${2:-1.5}
output=${3:-$model}

# folder for tmp files
mkdir -p "${this}/../computations/${output}"

# train
echo "Training model... ${model} [${output}]"
/usr/local/bin/crf_learn -c ${c} "${this}/../models/${model}" "${this}/../data/train.txt" "${this}/../computations/${output}/model" > /dev/null

# test
/usr/local/bin/crf_test -m "${this}/../computations/${output}/model" "${this}/../data/test.txt" > "${this}/../computations/${output}/comparison"

# evaluate
${this}/conlleval.pl -d '\t' < "${this}/../computations/${output}/comparison" > "${this}/../computations/${output}/performances"
head -n2 "${this}/../computations/${output}/performances"

# compute the errors
${this}/errors.py < "${this}/../computations/${output}/comparison" > "${this}/../computations/${output}/errors"
