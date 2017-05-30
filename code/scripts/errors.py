#!/usr/bin/env python3

#
# This Python script analyzes the predictions of a CRF++ model
# and outputs the sentences that contains prediction errors.
# This was used to come up with good features during the training.
#

import sys


def main():
    """
    Read the CRF++ prediction output from the standard input,
    compute the prediction errors and print them to the standard output.
    """

    # initialization
    line_number = 0
    errors = False
    current_phrase = []

    # read line by line
    for line in sys.stdin:
        line_number += 1
        line = line.replace('\n', '')

        # always store the last line
        current_phrase.append((line_number, line))

        # split different columns
        chunks = line.split('\t')
        l = len(chunks)

        # end phrase
        if l == 1:
            if errors:
                for n, p in current_phrase:
                    if p == '':
                        print('')
                    else:
                        print(str(n) + '\t' + p)
            errors = False
            current_phrase = []

        # check for errors
        else:
            assert l >= 3
            prediction = chunks[l - 1]
            real = chunks[l - 2]
            if prediction != real:
                errors = True


# entry point
if __name__ == "__main__":
    main()
