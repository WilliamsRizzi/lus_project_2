#!/usr/bin/env python3

import sys

def main():
    line_number = 0

    errors = False
    current_phrase = []
    start_index = 0

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

if __name__ == "__main__":
    main()
