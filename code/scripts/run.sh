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
n=$1
model="model_${n}"

# folder for tmp files
mkdir -p "computations/${model}"

# train
crf_learn "model/template_${n}" "data/train.txt" "computations/${model}/model"

# test
crf_test -m "computations/${model}/model" "data/test.txt" > "computations/${model}/comparison"

# evaluate
./scripts/conlleval.pl -d '\t' < "computations/${model}/comparison" > "computations/${model}/performances"
head -n2 "computations/${model}/performances"
