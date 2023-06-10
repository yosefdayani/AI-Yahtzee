from state import *
import random
import numpy as np
import itertools
import pandas as pd

NUM_CATEGORIES = 13
YAHTZEE_BONUS = 50
YAHTZEE_SCORE = 50
LARGE_STRAIGHT_SCORE = 40
LARGE_STRAIGHT_SETS = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
SMALL_STRAIGHT_SCORE = 30
SMALL_STRAIGHT_SETS = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
FULL_HOUSE_SET = {2, 3}
FULL_HOUSE_SCORE = 25
YAHTZEE_DRAW_NUM = 5
THREE_OF_A_KIND_NUM = 3
FOUR_OF_A_KIND_NUM = 4
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
CAT_INT_NAME = { 0:"ONES",
 1:"TWOS",
 2:"THREES",
 3:"FOURS",
 4:"FIVES",
 5:"SIXES",
 6:"THREE_OF_A_KIND",
 7:"FOUR_OF_A_KIND",
 8:"FULL_HOUSE",
 9:"SMALL_STRAIGHT",
10:"LARGE_STRAIGHT",
11:"YAHTZEE",
12:"CHANCE"}
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

NUMBER_CATEGORIES_SET = {ONES, TWOS, FOURS, THREES, FIVES, SIXES}
BONUS_THRESH = 63
NUMBER_BONUS = 35


def update_dice(prev_dice=(), keep=()):
    new_dice = []
    if keep == ():
        new_dice = [random.randint(1, 6) for x in range(5)]
    else:
        for i in range(5):
            if i not in keep:
                new_dice.append(random.randint(1, 6))
            else:
                new_dice.append(prev_dice[i])
    return new_dice


def generate_all_actions():
    actions = []
    for i in range(NUM_CATEGORIES):
        actions.append(Action(ActionType.PICK_CATEGORY, i))
    S = [j for j in range(5)]  # dice's indexes
    for i in range(5):  # subset's size (0-4) to keep the dice
        combs = list(itertools.combinations(S, i))
        for c in combs:
            actions.append(Action(ActionType.REROLL, c))
    return actions


class Game:
    def __init__(self):
        dice = [random.randint(1, 6) for x in range(5)]
        categories = [False] * NUM_CATEGORIES  # False if category is not filled already
        self.curr_state = State(dice, categories, self)
        self.all_actions = generate_all_actions()
        self.score = 0
        self.number_bonus = 0
        self.got_bonus = False
        self.CALC_SCORE_DICT = {0: self.calc_ones_score,
                                1: self.calc_twos_score,
                                2: self.calc_threes_score,
                                3: self.calc_fours_score,
                                4: self.calc_fives_score,
                                5: self.calc_sixes_score,
                                6: self.calc_three_of_a_kind_score,
                                7: self.calc_four_of_a_kind_score,
                                8: self.calc_full_house_score,
                                9: self.calc_small_straight_score,
                                10: self.calc_large_straight_score,
                                11: self.calc_yahtzee_score,
                                12: self.calc_chance_score}
        self.was_yahtzee = False

    def __str__(self):
        return self.curr_state.__str__() + f"Total_Score: {self.score}\nNumber Score: {self.number_bonus}\n" + \
               f"Was Yahtzee: {self.was_yahtzee}\n Got Bonus {self.got_bonus}\n\n"

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
            # print("pick category before dice change")
            # print(self)
            dice = update_dice()
            new_state = State(dice, self.curr_state.categories, self)
            self.curr_state = new_state
            # print("---------------")
            # print("dice after change in pick category")
            # print(dice)
            # print("###################")
        else:

            self.curr_state.dice = update_dice(self.curr_state.dice, action.info)
            self.curr_state.rerolls -= 1
            # print("after reroll")
            # print(self)

    def calc_score(self, category,dice=0):
        if dice:
            return self.CALC_SCORE_DICT[category](dice)
        else:
            return self.CALC_SCORE_DICT[category](self.curr_state.dice)
    def update_score(self, value, was_yahtzee_flag, number_bonus_flag):
        self.score += value
        if was_yahtzee_flag:
            self.was_yahtzee = True
        if number_bonus_flag:  # only updates the category points since value could include yahtzee bonus
            if value > YAHTZEE_BONUS:
                self.number_bonus += (value - YAHTZEE_BONUS)
            else:
                self.number_bonus += value
        # print(self.number_bonus)
        if not self.got_bonus and self.number_bonus > BONUS_THRESH:

            self.score += NUMBER_BONUS
            self.got_bonus = True

    def calc_ones_score(self,dice):
        """
        calculates the score for ones category and updates the score_1 variable.
        ones score = 1*(# of 1's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """

        base = dice.count(1)
        value = base
        if self.was_yahtzee and value == YAHTZEE_DRAW_NUM:
            value += YAHTZEE_BONUS
        if base + self.number_bonus >= BONUS_THRESH and not self.got_bonus:
            value += NUMBER_BONUS
        return value

    def calc_twos_score(self,dice):
        """
        calculates the score for twos category and updates the score_1 variable.
        twos score = 2*(# of 2's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = dice.count(2)
        base= 2 * count
        value = base
        if self.was_yahtzee and count == YAHTZEE_DRAW_NUM:
            value += YAHTZEE_BONUS
        if base+self.number_bonus>= BONUS_THRESH and not self.got_bonus:
            value+=NUMBER_BONUS
        return value

    def calc_threes_score(self,dice):
        """
        calculates the score for threes category and updates the score_1 variable.
        threes score = 3*(# of 3's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = dice.count(3)
        base = 3 * count
        value = base
        if self.was_yahtzee and count == YAHTZEE_DRAW_NUM:
            value += YAHTZEE_BONUS
        if base+self.number_bonus>= BONUS_THRESH and not self.got_bonus:
            value+=NUMBER_BONUS
        return value

    def calc_fours_score(self,dice):
        """
        calculates the score for fours category and updates the score_1 variable.
        fours score = 4*(# of 4's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = dice.count(4)
        base = 4 * count
        value = base
        if self.was_yahtzee and count == YAHTZEE_DRAW_NUM:
            value += YAHTZEE_BONUS
        if base+self.number_bonus>= BONUS_THRESH and not self.got_bonus:
            value+=NUMBER_BONUS
        return value

    def calc_fives_score(self,dice):
        """
        calculates the score for fives category and updates the score_1 variable.
        fives score = 5*(# of 5's in the draw) + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = dice.count(5)
        base = 5 * count
        value = base
        if self.was_yahtzee and count == YAHTZEE_DRAW_NUM:
            value += YAHTZEE_BONUS
        if base+self.number_bonus>= BONUS_THRESH and not self.got_bonus :
            value+=NUMBER_BONUS
        return value

    def calc_sixes_score(self,dice):
        """
        calculates the score for sixes category and updates the score_1 variable.
        sixes score = 6*(# of 6's in the draw) + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = dice.count(6)

        base =  6 * count
        value = base
        if self.was_yahtzee and count == YAHTZEE_DRAW_NUM:
            value += YAHTZEE_BONUS
        if base + self.number_bonus >= BONUS_THRESH and not self.got_bonus:
            value += NUMBER_BONUS
        return value

    def calc_chance_score(self,dice):
        """
        calculates the chance category score and updates score_2 variable
        chance_score = sum(draw) + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(dice).value_counts()
        max_count = counts.max()
        value = sum(dice)
        if max_count == YAHTZEE_DRAW_NUM and self.was_yahtzee:
            value += YAHTZEE_BONUS
        return value

    def calc_yahtzee_score(self,dice):
        """
        calculates the yahtzee category score and updates score_2 variable
        yahtzee_score = 50*I(draw is yahtzee)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(dice).value_counts()
        if YAHTZEE_DRAW_NUM in counts.values:
            return YAHTZEE_SCORE
        return 0

    def calc_large_straight_score(self,dice):
        """
        calculates the large_straight category score and updates score_2 variable
        large_straight_score = 40*I(draw is a 5 number straight)
        :param draw: the draw to calculate score for
        """
        draw_set = set(dice)
        for s in LARGE_STRAIGHT_SETS:
            if s.issubset(draw_set):
                return LARGE_STRAIGHT_SCORE
        return 0

    def calc_small_straight_score(self,dice):
        """
        calculates the small_straight category score and updates score_2 variable
        small_straight_score = 30*I(draw contains a 4 number straight)
        :param draw: the draw to calculate score for
        """
        draw_set = set(dice)
        for s in SMALL_STRAIGHT_SETS:
            if s.issubset(draw_set):
                return SMALL_STRAIGHT_SCORE
        return 0

    def calc_three_of_a_kind_score(self,dice):
        """
        calculates the three_of_a_kind category score and updates score_2 variable
        three_of_a_kind_score = sum(draw)*I(draw contains at least 3 of the same number)
                                + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(dice).value_counts()
        max_count = counts.max()
        value = 0
        if max_count >= THREE_OF_A_KIND_NUM:
            value = sum(dice)
            if max_count == YAHTZEE_DRAW_NUM and self.was_yahtzee:
                value += YAHTZEE_BONUS
        return value

    def calc_four_of_a_kind_score(self,dice):
        """
        calculates the four_of_a_kind category score and updates score_2 variable
        four_of_a_kind_score = sum(draw)*I(draw contains at least 4 of the same number)
                                + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(dice).value_counts()
        max_count = counts.max()
        value = 0
        if max_count >= FOUR_OF_A_KIND_NUM:
            value = sum(dice)
            if max_count == YAHTZEE_DRAW_NUM and self.was_yahtzee:
                value += YAHTZEE_BONUS
        return value

    def calc_full_house_score(self,dice):
        """
        calculates the full_house category score and updates score_2 variable
        full_house_score = 25*I(draw contains exactly 3 of the one number and 2 of another number)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(dice).value_counts()
        counts_set = set(counts)
        if FULL_HOUSE_SET.issubset(counts_set):
            return FULL_HOUSE_SCORE
        return 0

    def game_over(self):
        return False not in self.curr_state.categories


if __name__ == '__main__':

    game = Game()
    while not game.game_over():
        actions = game.curr_state.get_legal_actions()
        index = random.randint(0, len(actions) - 1)
        game.do_action(actions[index])
        a = 1
