import pdb
from pymonad import *
from functools import reduce

class Value(Monoid):
    # Value of a bit encoding represented by a tuple.
    # Tuple follows the format  (Just(digit), operator).
    # If digit is Nothing, then the representation only contains an operator.
    # Ex:
    # (6, '+') -> 6 +
    # (6, '_') -> 6
    # (N, '+') -> +
    # (6, '-') + (2, '*') = (4, '*')
    # (6, '_') + (6, '+') = (66, '+')
    # (6, '_') + (N, '-') = (6, '-')
    # (N, '-') + (N, '+') = (N, '-')
    # (N, '-') + (2, '_') = (2, '_')
    # (6, '+') + (N, '-') = (6, '+')

    @staticmethod
    def mzero():
        # Identity
        return Value((Nothing, '_'))

    def mplus(self, other):
        # Combination operator.
        self_digit = self.getValue()[0]
        self_op = self.getValue()[1]
        other_digit = other.getValue()[0]
        other_op = other.getValue()[1]

        if self_digit == Nothing:
            if other_digit == Nothing:
                if self_op == '_':
                    return other
                else:
                    return self
            else:
                return other

        elif self_op == '_':
            if other_digit == Nothing:
                return Value((self_digit, other_op))
            elif self_digit.getValue() == 0:
               return other 
            else:
                # Combine two numbers.
                # Ex: 4 _ 4 = 44
                # -4 _ 4 = -44
                # -4 _ -4 = -44
                return Value((Just(self_digit.getValue()/abs(self_digit.getValue())*
                             (abs(self_digit.getValue()) * 10 + abs(other_digit.getValue()))), other_op))

        elif other_digit == Nothing:
            return self

        elif self_op == '+':
            return Value((Just(self_digit.getValue() + other_digit.getValue()), other_op))
        elif self_op == '-':
            return Value((Just(self_digit.getValue() - other_digit.getValue()), other_op))
        elif self_op == '*':
            return Value((Just(self_digit.getValue() * other_digit.getValue()), other_op))
        elif self_op == '/':
            if other_digit.getValue() == 0:
                # Divide by zero.
                # Skip the operation.
                return self 
            else:
                return Value((Just(self_digit.getValue() // other_digit.getValue()), other_op))
        elif self_op == '%':
            if other_digit.getValue() == 0:
                # Modulo by zero.
                # Skip the operation.
                return self 
            return Value((Just(self_digit.getValue() % other_digit.getValue()), other_op))
        else:
            # Should never happen
            raise Exception("Invalid op.")

    def __str__(self):
        return "({}, {})".format(*self.getValue())

    def __repr__(self):
        return self.__str__()


# Utility functions.
def d(s):
    # Decode a string into Value.
    # String should follow format '(6, -)'
    tup = s[1:-1].split(',')
    return Value((Just(int(tup[0])) if tup[0] != 'N' else Nothing, tup[1].strip()))


@curry
def v(value):
    # Get the Value's digit.
    val = value.getValue()[0].getValue()
    return val if val else 0


def flatten(l):
    # From https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    return [item for sublist in l for item in sublist]


def split_four(xs):
    # Undefined behavior if xs % 4 != 0
    return [[xs[i] for i in range(j*4, j*4 + 4)] for j in range(len(xs)//4)]


@curry
def decode(chrom):
    chrom_map = {
        '0000' : Value((Just(0), '_')),
        '0001' : Value((Just(1), '_')),
        '0010' : Value((Just(2), '_')),
        '0011' : Value((Just(3), '_')),
        '0100' : Value((Just(4), '_')),
        '0101' : Value((Just(5), '_')),
        '0110' : Value((Just(6), '_')),
        '0111' : Value((Just(7), '_')),
        '1000' : Value((Just(8), '_')),
        '1001' : Value((Just(9), '_')),
        '1010' : Value((Nothing, '+')),
        '1011' : Value((Nothing, '-')),
        '1100' : Value((Nothing, '*')),
        '1101' : Value((Nothing, '/')),
        '1110' : Value((Nothing, '%')),
        '1111' : Value((Nothing, '_')),
    }
    return [chrom_map[''.join([str(x) for x in xs])] for xs in split_four(chrom)]


@curry
def evaluate_values(xs):
    return reduce(lambda x, y: x + y, xs)

# Evaluate a chromosome and return the digit value.
evaluate = v * evaluate_values * decode


# Reduce tokens and its extra is a DFA to generate printable expression to
# be displayed as the result. It cuts out extra tokens that gets removed when
# evaluated so that the result print out can be clean.
def reduce_tokens(x, ys):
    if not ys:
        if x in '0123456789':
            return x
        else:
            return ''
    if x in '0123456789':
        return x + reduce_tokens_after_digits(ys[0], ys[1:])
    else:
        return reduce_tokens(ys[0], ys[1:])


def reduce_tokens_after_digits(x, ys):
    if not ys:
        if x in '0123456789':
            return x
        else:
            return ''
    if x in '0123456789':
        return x + reduce_tokens_after_digits(ys[0], ys[1:])
    elif x in '+-*/%' and ys[0] in '+-*/%_':
        # Skip next token.
        return reduce_tokens_after_digits(x, ys[1:])
    elif x == '_' and ys[0] in '+-*/%_':
        return reduce_tokens_after_digits(ys[0], ys[1:])
    elif x in '/%' and ys[0] == '0':
        # Divide by zero.
        # Skip 0.
        return reduce_tokens_after_digits(x, ys[1:])
    elif x in '+-*/%_' and ys[0] in '0123456789':
        return x + reduce_tokens_after_digits(ys[0], ys[1:])
    else:
        # Should never happen.
        raise Exception("Uncaught pattern for reduce_tokens")


def printable_expression(xs):
    # Produce something printable for debugging.
    return ''.join(['{} {} '.format(v(x) if x.getValue()[0].getValue() != None else '', x.getValue()[1]) for x in xs])


def reduced_expression(exp):
    # Produce a printable that is suitable for displaying as a final solution.
    _exp = exp.replace(' ', '')
    return ' '.join(reduce_tokens(_exp[0], _exp[1:]))
