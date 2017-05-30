#!/usr/bin/env bash

#
# This script is used to convert the performances of some models
# to a LaTeX table to put in the report.
#

# parse the output of the evaluation script
function parse_conlleval() {
    sed -n 2p | sed 's/^.*precision: *\(.*\)%; recall: *\(.*\)%; FB1: *\(.*\)$/\1% \2% \3%/'
}

# parse the output of the evaluation script to extract only F1
function parse_f1() {
   parse_conlleval | cut -d ' ' -f 3
}

# format as a LaTeX table
function latex() {
    sed 's/ / \& /g' | sed 's/$/ \\\\/' | sed 's/_/\\_/g' | sed 's/%/\\%/g'
}

# extract the window size from the model name
function parse_window_size_words() {
    sed 's/\/performances$//'| sed 's/^.*words_window_\([0-9]\)_no_b/\1/'
}

# extract the window size from the model name
function parse_window_size() {
    sed 's/\/performances$//'| sed 's/^.*window_\([0-9]\)/\1/'
}

# extract the regularization parameter from the model name
function parse_regularization_parameter() {
    sed 's/\/performances$//'| sed 's/^.*_\(.*\)$/\1/'
}

# remove the new line from a string
function remove_new_line() {
    tr '\n' ' '
}

this=$(dirname $0)
computations="$this/../computations"
table="$this/../../report/table"
mkdir -p $table

echo -n "----------------------------------------"
echo -e "\n 1) model with words only"
echo "----------------------------------------"
echo "window, F1 (no bigrams), F1 (bigrams)"
for f in $computations/01_basic/*_no_b/performances; do
    window=$(echo $f | parse_window_size_words)
    echo -n $window
    echo -n ' '
    cat $f | parse_f1 | remove_new_line
    cat `echo $f | sed 's/_no_b//'` | parse_f1
done | tee >(latex > $table/01_words.tex)
echo -e "----------------------------------------\n"

echo -n "----------------------------------------"
echo -e "\n 2) model with words + POS"
echo "----------------------------------------"
echo "window, prec, rec, F1"
for f in $computations/02_intermediate/pos_*/performances; do
    window=$(echo $f | parse_window_size)
    echo -n $window
    echo -n ' '
    cat $f | parse_conlleval
done | tee >(latex > $table/02_pos.tex)
echo -e "----------------------------------------\n"

echo -n "----------------------------------------"
echo -e "\n 3) model with words + POS + stem"
echo "----------------------------------------"
echo "window, prec, rec, F1"
for f in $computations/02_intermediate/stem_*/performances; do
    window=$(echo $f | parse_window_size)
    echo -n $window
    echo -n ' '
    cat $f | parse_conlleval
done | tee >(latex > $table/03_stems.tex)
echo -e "----------------------------------------\n"

echo -n "----------------------------------------"
echo -e "\n 4) regularization"
echo "----------------------------------------"
echo "c, prec, rec, F1"
for f in $computations/04_regularization/manual_10_*/performances; do
    window=$(echo $f | parse_regularization_parameter)
    echo -n $window
    echo -n ' '
    cat $f | parse_conlleval
done | sort | tee >(latex > $table/04_regularization.tex)
echo -e "----------------------------------------\n"
