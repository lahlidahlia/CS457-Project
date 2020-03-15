from pymonad import *
import pdb
from random import random
from functools import reduce
from value import *

def generate_bits(num):
    return [(1 if random() > 0.5 else 0) for _ in range(num)]

@curry
def crossover(rate, xs, ys):
    point = int(random() * len(xs))
    return (xs[0:point] + ys[point:], ys[0:point] + xs[point:]) \
           if random() < rate else (xs, ys)

def flip(x):
    return 0 if x == 1 else 1

@curry
def mutate(rate, xs):
    return [(flip(x) if random() < rate else x) for x in xs]

def to_list(s):
    return [int(x) for x in s]

def to_str(xs):
    return ''.join(str(x) for x in xs)


if __name__ == '__main__':

    #new = Value((Just(6), '-')) + Value((Just(2), '*'))
    #print(new.getValue())
    #print(len(generate_bits(9*4)))

    bits = generate_bits(9*4)
    de = decode(bits)
    ev = evaluate_values(de)
    print(bits)
    print(split_four(bits))
    print(de)
    print(ev)
    pdb.set_trace()
