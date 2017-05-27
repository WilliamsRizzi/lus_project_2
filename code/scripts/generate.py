#!/usr/bin/env python3
import sys
import itertools

def single_token(start, stop, col):
    features = []
    for i in range(start, stop + 1):
        features.append('%x[{:d},{:d}]'.format(i, col))
    return features

def main():

    words = single_token(-4, 7, 0)
    pos = single_token(-3, 3, 1)
    lemma = single_token(-2, 2, 2)
    capitalized = single_token(0, 0, 3)

    single = words + pos + lemma + capitalized

    # combinations
    double = []
    for a,b in itertools.product(single, single):
        double.append('{}/{}'.format(a,b))

    for i, f in enumerate(single + double):
        print('U{:04d}:{}'.format(i, f))

    # bigrams
    print('B')

if __name__ == "__main__":
    main()
