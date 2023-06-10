import abc
from abc import ABC
import random

import game
import numpy as np
import itertools
import state
import ExpectiMaxTable

S = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
SUBS = [set(itertools.combinations(S, i)) for i in range(6)]


class Agent:
    def __init__(self):
        self.my_game = game.Game()

    @abc.abstractmethod
    def do_turn(self):
        return

    def pick_action(self):
        return


class GreedyAgent(Agent):

    def do_turn(self):
        return self.pick_action()

    def pick_action(self):
        action_score = dict()
        legal_actions = self.my_game.curr_state.get_legal_actions()
        for action in legal_actions:
            if action.action_type == state.ActionType.PICK_CATEGORY:  # if it needs to pick category
                action_score[action] = self.my_game.calc_score(action.info)  # action(type, category): max_score
        max_dice_roll = self.my_game.curr_state.dice
        max_action = max(action_score, key=action_score.get)
        chosen_category = max_action.info
        max_score = action_score[max_action]
        self.my_game.do_action(max_action)
        return chosen_category, max_score, max_dice_roll


class ReRollGreedyAgent(Agent):
    def do_turn(self):
        return self.pick_action()

    def pick_action(self):
        legal_actions = self.my_game.curr_state.get_legal_actions()
        action_score = dict()

        # choose to do re-roll, otherwise choose to do category and does nothing
        while 0.5 < random.random() and self.my_game.curr_state.rerolls > 0:
            re_roll_action = random.choice(legal_actions)
            if re_roll_action.action_type == state.ActionType.PICK_CATEGORY:  # if choose randomly to pick category
                return self.get_cat_score_dice(action_score, legal_actions)
            self.my_game.do_action(re_roll_action)

        # did all the re rolls that can be done or with probability 0.5 decided to choose category
        return self.get_cat_score_dice(action_score, legal_actions)

    def get_cat_score_dice(self, action_score, legal_actions):
        for action in legal_actions:
            if action.action_type == state.ActionType.PICK_CATEGORY:
                action_score[action] = self.my_game.calc_score(action.info)
        max_dice_roll = self.my_game.curr_state.dice
        max_action = max(action_score, key=action_score.get)
        chosen_category = max_action.info
        max_score = action_score[max_action]
        self.my_game.do_action(max_action)
        return chosen_category, max_score, max_dice_roll


class RandomAgent(Agent):

    def do_turn(self):
        return self.pick_action()

    def pick_action(self):
        action_category = []
        legal_actions = self.my_game.curr_state.get_legal_actions()
        for action in legal_actions:
            if action.action_type == state.ActionType.PICK_CATEGORY:  # if it needs to pick category
                action_category.append(action)  # action(type, category): max_score
        dice_roll = self.my_game.curr_state.dice
        chosen_action = random.choice(action_category)
        chosen_category = chosen_action.info
        score = self.my_game.calc_score(chosen_category)
        self.my_game.do_action(chosen_action)
        return chosen_category, score, dice_roll


class ExpectIMaxAgent(Agent):

    def do_turn(self):
        return self.pick_action(rerolls=2)

    def pick_action(self, rerolls=0):
        action_score = dict()
        actions = self.my_game.curr_state.get_legal_actions()
        dice = self.my_game.curr_state.dice
        pfunc = Table.probr2 if rerolls == 2 else Table.probr1
        for action in actions:
            action_score[action] = 0
            if action.action_type == state.ActionType.PICK_CATEGORY:
                action_score[action] = self.my_game.calc_score(action.info) / Table.AVGS[action.info]
            else:
                sub = [dice[i] for i in action.info]
                combs = list(SUBS[5 - len(sub)])
                print(1)
                for c in combs:
                    pass
                    roll = sub.copy()
                    roll.extend(c)
                    s = 0
                    for cat in game.CATEGORIES:
                        if self.my_game.curr_state.categories[cat] == False:
                            score = self.my_game.calc_score(cat, roll) / Table.AVGS[cat]
                            if score >= s:
                                s = score
                    action_score[action] += s * pfunc(c)
                print(1)
        max_action = max(action_score, key=action_score.get)
        if max_action.action_type == state.ActionType.PICK_CATEGORY:
            max_dice_roll = self.my_game.curr_state.dice
            max_category = max_action.info
            max_score = action_score[max_action] * Table.AVGS[max_action.info]
            self.my_game.do_action(max_action)
            return max_category, int(max_score), max_dice_roll
        else:
            print(dice)
            print(max_action.info)
            self.my_game.do_action(max_action)
            return self.pick_action(rerolls=rerolls - 1)


class RlAgent(Agent):

    def do_turn(self):
        return

    def pick_action(self):
        return


if __name__ == '__main__':
    agent = GreedyAgent()
    while not agent.my_game.game_over():
        agent.do_turn()
    print("score: ")
    print(agent.my_game.score)