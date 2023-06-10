from enum import Enum


class ActionType(Enum):
    PICK_CATEGORY = 1
    REROLL = 2


class Action:
    def __init__(self, action_type, info):
        self.action_type = action_type
        self.info = info

    def __str__(self):
        s = "keep" if self.action_type == ActionType.REROLL else ""
        return self.action_type.name + ": " + s + str(self.info)


class State:
    def __init__(self, dice, categories, game, rerolls=2):
        self.dice = dice
        self.categories = categories
        self.rerolls = rerolls
        self.game = game

    def __str__(self):
        return f"DICE: {self.dice}\nCategories: {self.categories}\nRerolls: {self.rerolls}"

    def get_legal_actions(self):
        actions = []
        for action in self.game.all_actions:
            if self.is_legal_action(action):
                actions.append(action)
        return actions

    def is_legal_action(self, action):
        if action.action_type == ActionType.REROLL and self.rerolls < 1:  # can't reroll
            return False
        if action.action_type == ActionType.PICK_CATEGORY and self.categories[action.info] is True:
            # category already chosen
            return False
        return True
