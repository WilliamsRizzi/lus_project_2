#!/usr/bin/env python3

#
# This Python script implements a simple genetic algorithm
# to select the best features for the CRF++ engine.
# Please checkout the report for a detailed description.
#

import hashlib
import subprocess
import os
from itertools import islice
from random import randint
import pickle

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

# folders, relative to the "code" folder
MODELS = 'models'
SCRIPTS = 'scripts'
COMPUTATIONS = 'computations'
INITIAL_POPULATION_FOLDER = 'initial_population'


def create_id(individual):
    """
    Generate a unique identifier for a set of features.
    This is done by sorting the features in alphabetically order,
    inserting a separator between them and computing a MD5 hash.
    This can be used to cache already done computations.
    :param individual: Population individual, representing a CRF++ template.
    :return: Unique ID for the individual.
    """
    features = sorted(individual)
    string = '#'.join(features)
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def evaluate(individual):
    """
    Compute the fitness function for the given individual.
    It materialized the CRF++ template, train it and measure the performances on the test set.
    This function makes use of the `run.sh` BASH script in this folder and CRF++ binaries installed on the system. 
    :param individual: Population individual, representing a CRF++ template.
    :return: F1 value on the test set, as a float.
    """

    # step 1: create the template file
    _id = create_id(individual)
    if not os.path.exists(MODELS):
        os.makedirs(MODELS)

    # check if I need to train this model
    performances_file = '%s/%s/performances' % (COMPUTATIONS, _id)
    if not os.path.exists(performances_file):

        # write the model, if needed
        with open('%s/%s' % (MODELS, _id), 'w') as f:
            f.write('# Unigrams\n')
            for i, line in enumerate(individual):
                f.write('U{:03d}:{}\n'.format(i, line))
            f.write('\n')
            f.write('# Bigrams\n')
            f.write('B\n')

        # step 2: train and test using CRF++
        subprocess.run('%s/run.sh %s' % (SCRIPTS, _id), shell=True)

    else:

        # there are already the results for this model... just read them
        print('Model already trained... %s' % _id)

    # step 3: read the performances
    result = None
    with open(performances_file) as f:
        for line in islice(f, 1, 2):
            result = float(line.split('FB1:')[1].strip())
    print('%s -> F1: %s' % (_id, result))

    # return the performances
    # NB: this must be a tuple
    # noinspection PyRedundantParentheses
    return (result,)


def random_feature(extended=False):
    """
    Generate a random feature for the CRF++ template.
    :param extended: If False, only the original features (word, POS, stem) are used.
    :return: Random feature.
    """

    # take boundaries
    row_window = 7 if extended else 4
    col_window = 10 if extended else 2

    # extract one tuple
    def make_single():
        return randint(-row_window, row_window), randint(0, col_window)

    # randomly pick complex feature
    # 60% -> order 1
    # 30% -> order 2
    # 10% -> order 3
    _type = randint(1, 10)
    if 1 <= _type <= 6:
        order = 1
    elif 7 <= _type <= 9:
        order = 2
    else:
        order = 3

    # make the feature
    features = []
    for i in range(order):
        row, col = make_single()
        feature = '%x[{:d},{:d}]'.format(row, col)
        features.append(feature)
    return '/'.join(features)


def mutate(individual, toolbox, n=1):
    """
    Generate a new individual starting from the given one and applying some random mutations.
    A mutation can be one of the following:
      - deletion of a random feature (to get rid of the redundant / not useful ones)
      - insertion of a new feature
      - substitution of a random feature with a newly generated one
    :param individual: Original individual to mutate. NB: the original individual is NOT modified,
                       instead it is cloned a the new one is modified.
    :param toolbox: DEAP toolbox, used to clone the individual.
    :param n: Upper bound to the number of mutations to apply. The real number is randomly chosen in [1, n].
    :return: A new individual, result of the mutation of the old one.
    """

    # make a copy of the individual
    mutant = toolbox.clone(individual)
    del mutant.fitness.values

    # randomly apply a mutation
    mutation = randint(1, 3)

    # apply n mutations of the same type
    m = randint(1, n)
    for i in range(m):

        # delete one element
        if mutation == 1:
            index = randint(0, len(mutant) - 1)
            mutant.pop(index)

        # insert a gene
        elif mutation == 2:
            gene = random_feature(extended=True)
            mutant.append(gene)

        # substitute
        else:
            index = randint(0, len(mutant) - 1)
            mutant.pop(index)
            gene = random_feature(extended=True)
            mutant.append(gene)

    # return it
    # NB: this must be a tuple
    # noinspection PyRedundantParentheses
    return (mutant,)


def load_population_guess(create_population, create_individual, directory):
    """
    Load the guess initial population from a group of CRF++ templates.
    This function iterates over all files in the target directory,
    loads all CRF++ templates found, remove the B feature (automatically added later)
    and convert each list of feature in a DEAP individual.
    :param create_population: Function used to convert a data structure to a DEAP population.
    :param create_individual: Function used to convert a data structure to a DEAP individual.
    :param directory: Directory where to find the CRF++ templates.
    :return: Population of individuals generated from the CRF++ templates.
    """

    # container for the population
    population = []

    # loop over all files in the directory
    for filename in os.listdir(directory):
        with open('%s/%s' % (directory, filename), 'r') as f:
            features = []
            for line in f:

                # remove spaces and \n
                stripped = line.strip()

                # skip comments
                if stripped.startswith('#'):
                    pass

                # parse unigrams
                elif stripped.startswith('U'):
                    cleaned = stripped.split(':')[1]
                    features.append(cleaned)

                # strip bigram
                elif stripped == 'B':
                    pass

                # check -> right syntax
                else:
                    assert stripped == ''

        # create the individual
        individual = create_individual(features)
        population.append(individual)

    # create the population
    return create_population(population)


# noinspection PyUnresolvedReferences
def main():
    """
    Generate and train a population of CRF++ templates to solve the concept tagging task.
    This script will use a genetic algorithm to generate and select the best features
    in order to maximize the performances of a CRF++ classifier on the concept tagging task.
    We use the Python DEAP library: https://github.com/DEAP/deap.
    NB: the parameters of the genetic algorithm are chosen empirically.
    """

    # the individual is simply a list of features...
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # initialize the DEAP toolbox
    toolbox = base.Toolbox()

    # define how to generate a new individual = iterate over random features
    toolbox.register("random_feature", random_feature)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_feature, n=15)

    # define the evaluation function... this calls the external script to train and evaluate the CRF model
    toolbox.register("evaluate", evaluate)

    # define the parameters to use for the genetic algorithm
    #   - how to perform mutations
    #   - how to mate 2 individuals
    #   - how to select the best individuals for the next epoch
    toolbox.register("mutate", mutate, toolbox=toolbox, n=3)
    toolbox.register("mate", tools.cxUniform, indpb=0.33)
    toolbox.register("select", tools.selTournament, tournsize=4)

    # population: combination of a random population and the initial guess
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("population_guess", load_population_guess, list, creator.Individual, INITIAL_POPULATION_FOLDER)

    # genetic algorithm:
    #   - load the initial guess for the population + add some completely random individuals
    #   - start the evolution (mutate, mate, select... loop)
    pop = toolbox.population_guess() + toolbox.population(n=6)
    _, log = algorithms.eaSimple(pop, toolbox, cxpb=0.3, mutpb=0.5, ngen=15)

    # print and save a summary of the evolution
    print(log.stream)
    with open('evolution_log.pickle', 'wb') as fp:
        pickle.dump(log, fp)


# entry point: launch the main
if __name__ == '__main__':
    main()
