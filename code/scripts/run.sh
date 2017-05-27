#!/usr/bin/env bash

# check the input parameters, exit if wrong input
if [[ ! "$#" == 1 ]]; then 
    echo "Wrong number of parameters."
	echo ""
	echo "Usage: $0 model_number"
    echo ""
    exit 1
fi

# extract the model to train
model=$1

# folder for tmp files
mkdir -p "computations/${model}"

# train
echo "Training model... ${model}"
/usr/local/bin/crf_learn -c 1.5 "models/${model}" "data/train.txt" "computations/${model}/model" > /dev/null

# test
/usr/local/bin/crf_test -m "computations/${model}/model" "data/test.txt" > "computations/${model}/comparison"

# evaluate
./scripts/conlleval.pl -d '\t' < "computations/${model}/comparison" > "computations/${model}/performances"
head -n2 "computations/${model}/performances"

# compute the errors
./scripts/errors.py < "computations/${model}/comparison" > "computations/${model}/errors"
