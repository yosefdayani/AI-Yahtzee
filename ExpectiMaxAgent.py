from AgentOne import Agent
import pandas as pd
import state
import ExpectiMaxTable
from multiset import FrozenMultiset
import itertools

S = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
SEPERATED_SUBS = [list(set(itertools.combinations(S, i))) for i in range(1, 6)]
ds1 = [pd.DataFrame(0, index=combs, columns=["probs", "scores"], dtype=float) for combs in
       SEPERATED_SUBS]
ds2 = [pd.DataFrame(0, index=combs, columns=["probs", "scores"], dtype=float) for combs in
       SEPERATED_SUBS]
for i in range(len(ds1)):
    for j, index in enumerate(ds1[i].index):
        ds1[i].iloc[j, 0] = ExpectiMaxTable.probr1(list(pd.Series(index).value_counts()))
        ds2[i].iloc[j, 0] = ExpectiMaxTable.probr2(list(pd.Series(index).value_counts()))


class ExpectiMaxAgent(Agent):
    """
    Yatzy ExpectiMax Agent
    """

    def __init__(self, avgs, throws):
        """
        loads pre-computed values for efficiency
        """
        super().__init__()
        self.avgs = avgs
        self.throws = throws
        self.cat_dict_order = ExpectiMaxTable.generate_dicts(self.avgs)

    def do_turn(self):
        return self.pick_action(rerolls=self.my_game.curr_state.rerolls)

    def pick_action(self, rerolls=0):
        global STATIC
        max_action = self.get_best_action(rerolls=rerolls)
        if max_action.action_type == state.ActionType.PICK_CATEGORY:
            max_dice_roll = self.my_game.curr_state.dice
            max_category = max_action.info
            max_score = self.my_game.calc_score(category=max_category)
            self.my_game.do_action(max_action)
            return max_category, max_score, max_dice_roll
        else:
            self.my_game.do_action(max_action)
            return self.pick_action(rerolls=rerolls - 1)

    def get_best_action(self, rerolls):
        actions = self.my_game.curr_state.get_legal_actions()
        best_action, best_score = None, -10
        for action in actions[::-1]:
            if action.action_type == state.ActionType.PICK_CATEGORY:
                score = self.my_game.calc_score(action.info) / self.avgs[action.info]
                if rerolls == 0:
                    score += self.throws[action.info]
            else:
                score = self.action_expectation(action, rerolls)
            if score > best_score:
                best_action, best_score = action, score
        return best_action

    def action_expectation(self, action, rerolls):
        """
        calculates the expected outcome of the given action and precomputed probabilities
        """
        dice = self.my_game.curr_state.dice
        sub = [dice[i] for i in action.info]
        ds = ds1 if rerolls == 1 else ds2
        d = ds[5 - len(sub) - 1]
        d = d.apply(lambda row: self.score(sub, row), axis=1)
        return (d["scores"] * d["probs"]).sum()

    def score(self, sub, row):
        index = row.name
        roll = sub.copy()
        roll.extend(list(index))
        sorted_categories = self.cat_dict_order[FrozenMultiset(roll)]
        category = False
        i = 0
        while not category:
            cat = sorted_categories[i]
            if self.my_game.curr_state.categories[cat] == False:
                category = True
            i += 1
        row["scores"] = self.my_game.calc_score(category=cat, dice=roll) / self.avgs[cat]
        return row



