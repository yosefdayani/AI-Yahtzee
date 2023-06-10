from tkinter import *
import os
from functools import partial
from tkinter import messagebox
import random
import numpy as np
import pandas as pd

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

CATEGORY_INT_DICT = {ONES: "Ones", TWOS: "Twos", THREES: "Threes", FOURS: 'Fours', FIVES: 'Fives',
                     SIXES: 'Sixes', THREE_OF_A_KIND: 'Three Of A Kind',
                     FOUR_OF_A_KIND: 'Four Of A Kind', FULL_HOUSE: 'Full House',
                     SMALL_STRAIGHT: 'Small Straight', LARGE_STRAIGHT: 'Large Straight',
                     YAHTZEE: 'Yahtzee', CHANCE: 'Chance'}
YAHTZEE_BONUS = 50
YAHTZEE_SCORE = 50
LARGE_STRAIGHT_SCORE = 40
LARGE_STRAIGHT_SETS = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
SMALL_STRAIGHT_SCORE = 30
SMALL_STRAIGHT_SETS = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
FULL_HOUSE_SET = {2, 3}
FULL_HOUSE_SCORE = 25
YAHTZEE_INDEX = 11
YAHTZEE_DRAW_NUM = 5
THREE_OF_A_KIND_NUM = 3
FOUR_OF_A_KIND_NUM = 4
ONES = 'Ones'
TWOS = 'Twos'
THREES = 'Threes'
FOURS = 'Fours'
FIVES = 'Fives'
SIXES = 'Sixes'
THREE_OF_A_KIND = 'Three Of A Kind'
FOUR_OF_A_KIND = 'Four Of A Kind'
FULL_HOUSE = 'Full House'
SMALL_STRAIGHT = 'Small Straight'
LARGE_STRAIGHT = 'Large Straight'
YAHTZEE = 'Yahtzee'
CHANCE = 'Chance'
CANVAS_DIMS = 400, 400
WIDTH, HEIGHT = 0, 1


class App(Frame):
    """
    Gui interface for Yatzy - nothing interesting AI-wise
    """
    def __init__(self, master, agent):
        self.real_yhatzee = False
        self.agent = agent
        self.CALC_SCORE_DICT = {ONES: self.calc_ones_score,
                                TWOS: self.calc_twos_score,
                                THREES: self.calc_threes_score,
                                FOURS: self.calc_fours_score,
                                FIVES: self.calc_fives_score,
                                SIXES: self.calc_sixes_score,
                                THREE_OF_A_KIND: self.calc_three_of_a_kind_score,
                                FOUR_OF_A_KIND: self.calc_four_of_a_kind_score,
                                FULL_HOUSE: self.calc_full_house_score,
                                SMALL_STRAIGHT: self.calc_small_straight_score,
                                LARGE_STRAIGHT: self.calc_large_straight_score,
                                YAHTZEE: self.calc_yahtzee_score,
                                CHANCE: self.calc_chance_score}
        super().__init__()
        self.master = master
        self.dieImages = []
        for i in range(1, 7):
            file_path = os.path.join(os.path.curdir, 'dice', '{}.gif'.format(i))
            self.dieImages.append(PhotoImage(file=file_path))
        self.categories = [ONES, TWOS, THREES, FOURS, FIVES, SIXES, THREE_OF_A_KIND, FOUR_OF_A_KIND,
                           FULL_HOUSE,
                           SMALL_STRAIGHT, LARGE_STRAIGHT, YAHTZEE, CHANCE]
        self.score_1, self.score_2, self.pc_score = 0, 0, 0

        self.filled_categories = {cat: False for cat in self.categories}
        self.buttonFrame = Frame(self.master)
        self.buttonFrame.grid(sticky="SW")
        self.rollButton = Button(self.buttonFrame, text="Roll Dice", font=('Impact', 30),
                                 command=partial(self.make_turn))
        self.rollButton.grid(row=0, column=0, rowspan=6, sticky='news')
        self.gameButtons = {}
        self.filled = 0
        mcol = 1
        mrow = 0
        for t in self.categories:
            self.gameButtons[t] = Button(self.buttonFrame, text=t,
                                         command=partial(self.picked_category, t), state=DISABLED)
            self.gameButtons[t].grid(row=mrow, column=mcol, sticky='news')
            mcol += 1
            if mcol == 3:
                mcol = 1
                mrow += 1
        self.displaysFrame = Frame(self.master)
        self.displaysFrame.grid(row=0, column=2, rowspan=3)
        self.displays = {}
        self.displaysFrame2 = Frame(self.master)
        self.displaysFrame2.grid(row=0, column=4, rowspan=3)
        self.displays2 = {}
        self.score_player = Label(self.displaysFrame,
                                  text="PLAYER: " + str(self.score_1 + self.score_2),
                                  font=('Impact', 30))
        self.score_player.grid(row=0, column=1, sticky='W')
        self.displays["PLAYER"] = [self.score_player]
        self.pc_score_label = Label(self.displaysFrame2, text="PC: " + str(self.pc_score),
                                    font=('Impact', 30))
        self.pc_score_label.grid(row=0, column=1, sticky='W')
        self.displays["PC"] = [self.pc_score_label]
        for r, i in enumerate(self.categories):
            t = Label(self.displaysFrame, text=i, font=('Impact', 20))
            c = Canvas(self.displaysFrame, height=55, width=280, bg='orange')
            g = Label(self.displaysFrame, text="0", font=('Impact', 20), fg="green")

            t.grid(row=r + 1, column=0, sticky='W')
            c.grid(row=r + 1, column=1, sticky='W')
            g.grid(row=r + 1, column=2, sticky="W")
            self.displays[i] = [t, c, g]
            q = Label(self.displaysFrame2, text=i, font=('Impact', 20))
            b = Canvas(self.displaysFrame2, height=55, width=280, bg='orange')
            d = Label(self.displaysFrame2, text="0", font=('Impact', 20), fg="red")
            q.grid(row=r + 1, column=0, sticky='W')
            b.grid(row=r + 1, column=1, sticky='W')
            d.grid(row=r + 1, column=2, sticky="W")
            self.displays2[i] = [q, b, d]

        self.keep = [False] * 5
        self.rerolled = 0
        self.score_1_bonus = False

    def picked_category(self, category):
        self.filled_categories[category] = True
        for cat in self.categories:
            self.gameButtons[cat].configure(state=DISABLED)
        roll = [i + 1 for i in self.dieRolls]
        curr_score = self.score_2 + self.score_1
        self.update_score(category, roll)
        if self.score_1 >= 63 and self.score_1_bonus == False:
            self.score_1 += 35
            self.score_1_bonus = True
        self.score_player.destroy()
        self.score_player = Label(self.displaysFrame,
                                  text="PLAYER: " + str(self.score_1 + self.score_2),
                                  font=('Impact', 30))
        self.score_player.grid(row=0, column=1, sticky='W')
        for i in range(5):
            self.displays[category][1].create_image((30 + 55 * i, 30),
                                                    image=self.dieImages[self.dieRolls[i]])
            self.keep_buttons[i].destroy()
        self.rollButton.configure(state=ACTIVE)
        self.reroll_button.configure(state=DISABLED)

        self.rerolled = 0
        self.displays[category][2].destroy()
        self.displays[category][2] = Label(self.displaysFrame,
                                           text=f"{self.score_1 + self.score_2 - curr_score}",
                                           font=('Impact', 20), fg="green")
        self.displays[category][2].grid(row=self.categories.index(category) + 1, column=2,
                                        sticky="W")
        self.filled += 1
        self.agent_turn()
        if self.filled == 13:
            self.game_over()

    def agent_turn(self):
        cat, currscore, roll = self.agent.do_turn()
        cat,roll = CATEGORY_INT_DICT[cat],np.array(roll)-1
        self.pc_score += currscore
        self.pc_score_label.destroy()
        self.pc_score_label = Label(self.displaysFrame2, text="PC: " + str(self.pc_score),
                                    font=('Impact', 30))
        self.pc_score_label.grid(row=0, column=1, sticky='W')
        self.displays2[cat][2].destroy()
        self.displays2[cat][2] = Label(self.displaysFrame2,
                                       text=f"{currscore}",
                                       font=('Impact', 20), fg="red")
        self.displays2[cat][2].grid(row=self.categories.index(cat) + 1, column=2,
                                    sticky="W")
        for i in range(5):
            self.displays2[cat][1].create_image((30 + 55 * i, 30),
                                                image=self.dieImages[roll[i]])

    def game_over(self):
        dif = self.score_2 + self.score_1 - self.pc_score
        if dif>0:
            text = "You Win!"
        elif dif < 0:
            text = "You Lose..."
        else:
            text = "It's A Draw"
        messagebox.showinfo("Game Over", text)

    def update_score(self, category, roll):
        self.CALC_SCORE_DICT[category](roll)

    def make_turn(self):
        self.rollButton.configure(state=DISABLED)
        for category in self.categories:
            if self.filled_categories[category] == False:
                self.gameButtons[category].configure(state=ACTIVE)
        self.dieRolls = [random.randint(0, 5) for x in range(5)]
        self.keep_buttons = []
        for i in range(5):
            self.keep_buttons.append(Button(command=partial(self.keep_button, self.keep_buttons, i),
                                            image=self.dieImages[self.dieRolls[i]], bg="gray"))
            self.keep_buttons[i].place(x=30 + 55 * i, y=50)
        self.reroll_button = Button(self.buttonFrame,
                                    command=partial(self.reroll, self.keep_buttons),
                                    text="Reroll", font=('Impact', 30))
        self.reroll_button.grid(row=12, column=0, sticky="w")
        self.keep = [False] * 5

    def reroll(self, keep_buttons):
        self.rerolled += 1
        destroyed = sum(self.keep)
        if self.rerolled == 2:
            self.reroll_button.configure(state=DISABLED)
        for i in range(5):
            if self.keep[i] == False:
                keep_buttons[i].destroy()
                destroyed += 1
                self.dieRolls[i] = random.randint(0, 5)
                keep_buttons[i] = Button(command=partial(self.keep_button, keep_buttons, i),
                                         image=self.dieImages[self.dieRolls[i]], bg="gray")
                keep_buttons[i].place(x=30 + 55 * i, y=50)

    def keep_button(self, button_list, i):
        if button_list[i].cget("bg") == "red":
            button_list[i].configure(bg="gray")
            self.keep[i] = False
        else:
            button_list[i].configure(bg="red")
            self.keep[i] = True

    def calc_ones_score(self, draw):
        """
        calculates the score for ones category and updates the score_1 variable.
        ones score = 1*(# of 1's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        value = draw.count(1)
        if self.filled_categories[YAHTZEE] is True and self.real_yhatzee and len(set(draw)) == 1:
            self.score_2 += YAHTZEE_BONUS
        self.score_1 += value

    def calc_twos_score(self, draw):
        """
        calculates the score for twos category and updates the score_1 variable.
        twos score = 2*(# of 2's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = draw.count(2)
        value = 2 * count
        if self.filled_categories[YAHTZEE] is True and self.real_yhatzee and len(set(draw)) == 1:
            self.score_2 += YAHTZEE_BONUS
        self.score_1 += value

    def calc_threes_score(self, draw):
        """
        calculates the score for threes category and updates the score_1 variable.
        threes score = 3*(# of 3's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = draw.count(3)
        value = 3 * count
        if self.filled_categories[YAHTZEE] is True and self.real_yhatzee and len(set(draw)) == 1:
            self.score_2 += YAHTZEE_BONUS
        self.score_1 += value

    def calc_fours_score(self, draw):
        """
        calculates the score for fours category and updates the score_1 variable.
        fours score = 4*(# of 4's in the draw)+ 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = draw.count(4)
        value = 4 * count
        if self.filled_categories[YAHTZEE] is True and self.real_yhatzee and len(set(draw)) == 1:
            self.score_2 += YAHTZEE_BONUS
        self.score_1 += value

    def calc_fives_score(self, draw):
        """
        calculates the score for fives category and updates the score_1 variable.
        fives score = 5*(# of 5's in the draw) + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = draw.count(5)
        value = 5 * count
        if self.filled_categories[YAHTZEE] is True and self.real_yhatzee and len(set(draw)) == 1:
            self.score_2 += YAHTZEE_BONUS
        self.score_1 += value

    def calc_sixes_score(self, draw):
        """
        calculates the score for sixes category and updates the score_1 variable.
        sixes score = 6*(# of 6's in the draw) + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        count = draw.count(6)
        value = 6 * count
        if self.filled_categories[YAHTZEE] is True and self.real_yhatzee and len(set(draw)) == 1:
            self.score_2 += YAHTZEE_BONUS
        self.score_1 += value

    def calc_chance_score(self, draw):
        """
        calculates the chance category score and updates score_2 variable
        chance_score = sum(draw) + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(draw).value_counts()
        max_count = counts.max()
        value = sum(draw)
        if max_count == YAHTZEE_DRAW_NUM and self.filled_categories[
            YAHTZEE] is True and self.real_yhatzee:
            value += YAHTZEE_BONUS
        self.score_2 += value

    def calc_yahtzee_score(self, draw):
        """
        calculates the yahtzee category score and updates score_2 variable
        yahtzee_score = 50*I(draw is yahtzee)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(draw).value_counts()
        if YAHTZEE_DRAW_NUM in counts.values:
            self.score_2 += YAHTZEE_SCORE
            self.real_yhatzee = True

    def calc_large_straight_score(self, draw):
        """
        calculates the large_straight category score and updates score_2 variable
        large_straight_score = 40*I(draw is a 5 number straight)
        :param draw: the draw to calculate score for
        """
        draw_set = set(draw)
        for s in LARGE_STRAIGHT_SETS:
            if s.issubset(draw_set):
                self.score_2 += LARGE_STRAIGHT_SCORE

    def calc_small_straight_score(self, draw):
        """
        calculates the small_straight category score and updates score_2 variable
        small_straight_score = 30*I(draw contains a 4 number straight)
        :param draw: the draw to calculate score for
        """
        draw_set = set(draw)
        for s in SMALL_STRAIGHT_SETS:
            if s.issubset(draw_set):
                self.score_2 += SMALL_STRAIGHT_SCORE
                break

    def calc_three_of_a_kind_score(self, draw):
        """
        calculates the three_of_a_kind category score and updates score_2 variable
        three_of_a_kind_score = sum(draw)*I(draw contains at least 3 of the same number)
                                + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(draw).value_counts()
        max_count = counts.max()
        if max_count >= THREE_OF_A_KIND_NUM:
            value = sum(draw)
            if max_count == YAHTZEE_DRAW_NUM and self.filled_categories[
                YAHTZEE] is True and self.real_yhatzee:
                value += YAHTZEE_BONUS
            self.score_2 += value

    def calc_four_of_a_kind_score(self, draw):
        """
        calculates the four_of_a_kind category score and updates score_2 variable
        four_of_a_kind_score = sum(draw)*I(draw contains at least 4 of the same number)
                                + 50*I(draw is yahtzee and yahtzee already filled)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(draw).value_counts()
        max_count = counts.max()
        if max_count >= FOUR_OF_A_KIND_NUM:
            value = sum(draw)
            if max_count == YAHTZEE_DRAW_NUM and self.filled_categories[
                YAHTZEE] is True and self.real_yhatzee:
                value += YAHTZEE_BONUS
            self.score_2 += value

    def calc_full_house_score(self, draw):
        """
        calculates the full_house category score and updates score_2 variable
        full_house_score = 25*I(draw contains exactly 3 of the one number and 2 of another number)
        :param draw: the draw to calculate score for
        """
        counts = pd.Series(draw).value_counts()
        counts_set = set(counts)
        if FULL_HOUSE_SET.issubset(counts_set):
            self.score_2 += FULL_HOUSE_SCORE

# import ExpectiMaxTable
# from ExpectiMaxAgent import ExpectiMaxAgent
# root = Tk()
# myapp = App(root,ExpectiMaxAgent(ExpectiMaxTable.AVGS,ExpectiMaxTable.THROWS))
# myapp.mainloop()
