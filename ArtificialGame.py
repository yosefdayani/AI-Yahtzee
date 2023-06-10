from game import *
import multiset
import numpy as np
import random

SMALL_STRAIGHT_DICES = list(set([multiset.FrozenMultiset([i+1,i+2,i+3,i+4,k+1]) for i in range(3) for k in range(6)]))
LARGE_STRAIGHT_DICES = list(set([multiset.FrozenMultiset([i+j+1 for j in range(5)]) for i in range(2)]))
YATSY_DICES = list(set([multiset.FrozenMultiset([i+1 for j in range(5)]) for i in range(6)]))
THREE_DICES = list(set([multiset.FrozenMultiset([i+1,i+1,i+1,j+1,k+1]) for i in range(2,6) for j in range(6) for k in range(6)]))
FOUR_DICES = list(set([multiset.FrozenMultiset([i+1,i+1,i+1,i+1,j+1]) for i in range(2,6) for j in range(6)]))
FULL_HOUSE_DICES = list(set([multiset.FrozenMultiset([i+1,i+1,i+1,j+1,j+1]) for i in range(6) for j in range(i+1)]))
SIXES_DICES_3 =  set([multiset.FrozenMultiset([6,6,6,j+1,k+1]) for i in range(6) for j in range(6) for k in range(6)])
SIXES_DICES_4=set([multiset.FrozenMultiset([6,6,6,6,j+1]) for i in range(6) for j in range(6)])
SIXES_DICES = list(SIXES_DICES_3.union(SIXES_DICES_4))
FIVES_DICES_3 =  set([multiset.FrozenMultiset([5,5,5,j+1,k+1]) for i in range(6) for j in range(6) for k in range(6)])
FIVES_DICES_4=set([multiset.FrozenMultiset([5,5,5,5,j+1]) for i in range(6) for j in range(6)])
FIVES_DICES = list(FIVES_DICES_3.union(FIVES_DICES_4))
FOURS_DICES_3 =  set([multiset.FrozenMultiset([4,4,4,j+1,k+1]) for i in range(6) for j in range(6) for k in range(6)])
FOURS_DICES_4=set([multiset.FrozenMultiset([4,4,4,4,j+1]) for i in range(6) for j in range(6)])
FOURS_DICES = list(FOURS_DICES_3.union(FOURS_DICES_4))
THREES_DICES_3 =  set([multiset.FrozenMultiset([3,3,3,j+1,k+1]) for i in range(6) for j in range(6) for k in range(6)])
THREES_DICES_4=set([multiset.FrozenMultiset([3,3,3,3,j+1]) for i in range(6) for j in range(6)])
THREES_DICES = list(THREES_DICES_3.union(THREES_DICES_4))
TWOS_DICES_3 =  set([multiset.FrozenMultiset([2,2,2,j+1,k+1]) for i in range(6) for j in range(6) for k in range(6)])
TWOS_DICES_4=set([multiset.FrozenMultiset([2,2,2,2,j+1]) for i in range(6) for j in range(6)])
TWOS_DICES = list(TWOS_DICES_3.union(TWOS_DICES_4))
ONES_DICES_3 =  set([multiset.FrozenMultiset([1,1,1,j+1,k+1]) for i in range(6) for j in range(6) for k in range(6)])
ONES_DICES_4=set([multiset.FrozenMultiset([1,1,1,1,j+1]) for i in range(6) for j in range(6)])
ONES_DICES = list(ONES_DICES_3.union(ONES_DICES_4))
CHANCE_DICES = [[6,5,4,6,5]]
GOOD_DICES = [ONES_DICES,TWOS_DICES,THREES_DICES,FOURS_DICES,FIVES_DICES,SIXES_DICES,THREE_DICES,FOUR_DICES,FULL_HOUSE_DICES,SMALL_STRAIGHT_DICES,LARGE_STRAIGHT_DICES,YATSY_DICES,CHANCE_DICES]


def print_sets_of_sets(s):
    print([list(k) for k in s])

from state import *

class ArtificialGame(Game):
    def __init__(self):
        super().__init__()
        dice = self.update_dice([False]*13)
        categories = [False] * NUM_CATEGORIES  # False if
        self.curr_state = State(dice, categories, self)

    def do_action(self, action):
        if action.action_type == ActionType.PICK_CATEGORY:
            value = self.calc_score(action.info)
            self.curr_state.categories[action.info] = True
            was_yahtzee_flag = False
            number_bonus_flag = False
            if action.info == YAHTZEE and value > 0:
                was_yahtzee_flag = True
            if action.info in NUMBER_CATEGORIES_SET:
                number_bonus_flag = True
            self.update_score(value, was_yahtzee_flag, number_bonus_flag)
            dice = self.update_dice(self.curr_state.categories)
            new_state = State(dice, self.curr_state.categories, self)
            self.curr_state = new_state
        else:
            self.curr_state.dice = update_dice(self.curr_state.dice, action.info)
            self.curr_state.rerolls -= 1
    def update_dice(self,categories):
        free_categories = [i for i, cat in enumerate(categories) if cat == False]
        if free_categories:
            chosen_category = np.random.choice(free_categories)
            dices = GOOD_DICES[chosen_category]
            return list(dices[np.random.multinomial(1,[1/len(dices)*len(dices)]).argmax()])


