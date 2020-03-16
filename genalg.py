from random import random
from bits import *
from value import *


def fitness(child, target):
    return 1/(abs(target - evaluate(child)) + 0.000001)


def first_generation(num_child, num_bits):
    return [generate_bits(num_bits) for _ in range(num_child)]

def assign_fitness(generation, target):
    # Input generation is list of children.
    # Output {child : fitness, ...}
    return {to_str(child):fitness(child, target) for child in generation}


def roulette(generation):
    # generation is {child : fitness, ...}
    fit_sum = sum(generation.values())
    return roulette_(iter(generation.items()), random(), fit_sum, 0)


def roulette_(gen_iter, chosen_prob, fit_sum, current_prob):
    n = next(gen_iter)
    current_prob += n[1]/fit_sum
    return n[0] if chosen_prob < current_prob \
                else roulette_(gen_iter, chosen_prob, fit_sum, current_prob)


def generate_chrom(_mutate, _crossover, generation):
    # generation is {child : fitness, ...}
    cross = _crossover(to_list(roulette(generation)), to_list(roulette(generation)))
    return [_mutate(cross[0]), _mutate(cross[1])]


def new_generation(from_gen, amount, _mutate, _crossover):
    # from_gen is {child : fitness, ...}
    return flatten([[child for child in generate_chrom(_mutate, _crossover, from_gen)] 
             for _ in range(amount//2)])


def get_max(gen):
    # Shortened function to get the highest fitness chromosome.
    return max(gen, key=gen.get)

def gen_alg(_mutate, _crossover, gen_size, target, generation):
    # Main loop. Generate new generations and stop when an answer is found.
    fit_gen = assign_fitness(generation, target)
    return decode(to_list(get_max(fit_gen))) \
           if evaluate(get_max(fit_gen)) == target \
           else gen_alg(_mutate, _crossover, gen_size, target,
                         new_generation(fit_gen, 
                                        gen_size, 
                                        _mutate, 
                                        _crossover))
