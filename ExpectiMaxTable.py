# Helper file for the ExpectimaxAgent

import math
import pandas as pd
import itertools
import game
from multiset import FrozenMultiset
from itertools import combinations
from scipy.stats import multinomial

# T
THROWS = [0.5738623046875001, 0.19542480468749998, -0.0600205078125, -0.07894238281250002,
          -0.0884033203125, -0.0884033203125, -0.06948144531249999, -0.050559570312499996,
          -0.0884033203125, -0.0884033203125, 0.05351074218749999, 0.4792529296875,
          -0.06948144531249999]
# W
AVGS = [13.452146615240778, 11.614320561125353, 8.857581479952202, 11.614320561125353,
        13.642957484970204, 17.127798723471642, 22.641276885817938, 21.722363858760218,
        22.641276885817938, 36.42497229168367, 18.04671175052936, 4.263016344663628,
        27.235842021106514]
S = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
FIVES_SET = list(set(itertools.combinations(S, 5)))
SUBS = [list(set(itertools.combinations(S, i))) for i in range(1, 6)]
SUBS = [inner for outer in SUBS for inner in outer]
OCCURS = {FrozenMultiset(pd.Series(s).value_counts()) for s in SUBS}

NORMALIZATION_CONSTANTS = [1.8333333333333335, 3.1527777777777772, 5.2483281893004134,
                           8.243602109053505, 12.597779393226372]
for i in range(2, 6):
    SUBS.extend(list(set(itertools.combinations(S, i))))

ONES = 0
TWOS = 1
THREES = 2
FOURS = 3
FIVES = 4
SIXES = 5
THREE_OF_A_KIND = 6
FOUR_OF_A_KIND = 7
FULL_HOUSE = 8
SMALL_STRAIGHT = 9
LARGE_STRAIGHT = 10
YAHTZEE = 11
CHANCE = 12
CATEGORIES = [ONES,
              TWOS,
              THREES,
              FOURS,
              FIVES,
              SIXES,
              THREE_OF_A_KIND,
              FOUR_OF_A_KIND,
              FULL_HOUSE,
              SMALL_STRAIGHT,
              LARGE_STRAIGHT,
              YAHTZEE,
              CHANCE]
CATEGORY_INT_DICT = {ONES: "Ones", TWOS: "Twos", THREES: "Threes", FOURS: 'Fours', FIVES: 'Fives',
                     SIXES: 'Sixes', THREE_OF_A_KIND: 'Three Of A Kind',
                     FOUR_OF_A_KIND: 'Four Of A Kind', FULL_HOUSE: 'Full House',
                     SMALL_STRAIGHT: 'Small Straight', LARGE_STRAIGHT: 'Large Straight',
                     YAHTZEE: 'Yahtzee', CHANCE: 'Chance'}


# s and c are occurrences vectors, for example s=[1,2,1] means that s is a multi set with
# 3 different elements, one of them occurred twice  (the specific values of the element are
# irrelevant since the dices are fair)
def probr1(s):
    """
    probability of achieving s in one reroll
    """
    if len(s) == 0:
        return 1
    rv = multinomial(sum(s), [1 / 6] * 6)
    zeros = [0] * (6 - len(s))
    copys = s.copy()
    copys.extend(zeros)
    return rv.pmf(copys)


def combinations(s, i):
    """
    return all sub combinations of s off length i
    """
    l = []
    s = list(s)
    for j in range(len(s)):
        for k in range(s[j]):
            l.append(j)
    combs = set(itertools.combinations(l, i))
    return [list(pd.Series(c).value_counts()) if len(c) > 0 else [] for c in combs]


def remainder(s, c):
    """
    action is saving c from s, returns the complement of c with respect to s
    """
    l = [s[i] - c[i] if i < len(c) else s[i] for i in range(len(s))]
    return [i for i in l if i != 0]


def probr2(s):
    """
    probability of achieving s in two rerolls
    """
    p = 0
    s = sorted(s, reverse=True)
    for i in range(0, sum(s) + 1):
        combs = combinations(s, i)
        for c in combs:
            j = 6 - (len(s) - len(c))
            c = sorted(c, reverse=True)
            for k in range(len(c)):
                if c[k] != s[k]:
                    j -= 1
            p += comb(sum(s), i) * probr1(c) * ((j / 6) ** (sum(s) - sum(c))) * probr1(
                remainder(s, c))
    return p / NORMALIZATION_CONSTANTS[sum(s) - 1]


def comb(n, k):
    """
    n choose k
    """
    return math.factorial(n) / (math.factorial(n - k) * math.factorial(k))


def generate_dicts(avgs):
    """
    generates precomputed values to for the ExpectiMax agent
    :return:
    """
    g = game.Game()
    cat_dict_order = dict()
    for sub in FIVES_SET:
        cat_order = {cat: g.calc_score(category=cat, dice=sub) / avgs[cat] for cat in CATEGORIES}
        sorted_cat = sorted(cat_order.keys(), key=cat_order.get, reverse=True)
        cat_dict_order[FrozenMultiset(sub)] = sorted_cat
    return cat_dict_order
