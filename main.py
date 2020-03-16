from random import random
from genalg import *
import pdb
import sys


if __name__ == '__main__':
    CROSSOVER_RATE=0.7
    MUTATE_RATE=0.02
    GEN_SIZE=200
    TARGET=int(random() * 100) if len(sys.argv) != 2 else int(sys.argv[1])
    NUM_BITS=9*4

    result = gen_alg(mutate(MUTATE_RATE), crossover(CROSSOVER_RATE), GEN_SIZE,
                   TARGET, first_generation(GEN_SIZE, NUM_BITS))

    print("TARGET: {}\n{} = {}".format(TARGET, reduced_expression(printable_expression(result)), TARGET))
