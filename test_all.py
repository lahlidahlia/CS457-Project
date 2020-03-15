from bits import *
from value import *
import pytest


def test_decode():
    assert d('(6, -)') == Value((Just(6), '-'))


def test_value():
    assert d('(6, -)') + d('(2, *)') == d('(4, *)')
    assert d('(6, _)') + d('(6, +)') == d('(66, +)')
    assert d('(6, _)') + d('(N, -)') == d('(6, -)')
    assert d('(N, -)') + d('(N, +)') == d('(N, -)')
    assert d('(N, -)') + d('(2, _)') == d('(2, _)')
    assert d('(6, +)') + d('(N, -)') == d('(6, +)')
    assert d('(6, /)') + d('(0, -)') == d('(6, /)')
    assert d('(0, _)') + d('(5, -)') == d('(5, -)')
    assert d('(0, _)') + d('(0, +)') == d('(0, +)')
    assert d('(N, _)') + d('(5, +)') == d('(5, +)')
    assert d('(N, _)') + d('(N, +)') == d('(N, +)')
    # Identity
    assert d('(N, _)') + d('(N, +)') == d('(N, +)')
    assert d('(6, +)') + d('(N, _)') == d('(6, +)')
    assert d('(6, _)') + d('(N, _)') == d('(6, _)')

def test_evaluate():
    # 6 + 6
    assert evaluate([0,1,1,0, 1,0,1,0, 0,1,1,0]) == 12
    # % + + * - _ * + %
    assert evaluate([1,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0]) == 0

def test_reduced_expression():
    assert reduced_expression('6 _ 1 _  _ 3 _  - 9 _  % 8 _ 4 _') == '6 _ 1 _ 3 - 9 % 8 _ 4'



def test_bits():
    assert len(generate_bits(5)) == 5
    assert split_four([0,0,0,0,1,1,1,1,0,0,0,0]) == \
           [[0,0,0,0],[1,1,1,1],[0,0,0,0]]


#def test_crossover():
#    # I can't test this because there's randomness in cross point.


def test_mutate():
    assert mutate(1, [0,0,0,0]) == [1,1,1,1]
