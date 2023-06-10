import pytest
import game
import AgentOne
import state


def test_calc_scores():
    calc_one_score_test()
    calc_two_score_test()
    calc_three_score_test()
    calc_four_score_test()
    calc_five_score_test()
    calc_six_score_test()
    calc_large_straight_score_test()
    calc_small_straight_score_test()
    calc_full_house_score_test()
    calc_yahtzee_score_test()
    calc_chance_score_test()
    calc_three_of_a_kind_score_test()
    calc_four_of_a_kind_score_test()


def calc_two_score_test():
    my_game = game.Game()
    dice = [1, 1, 1, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(1, dice) == old_score + 4


def calc_one_score_test():
    my_game = game.Game()
    dice = [1, 1, 1, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(0, dice) == old_score + 3


def calc_three_score_test():
    my_game = game.Game()
    dice = [1, 3, 3, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(2, dice) == old_score + 6


def calc_four_score_test():
    my_game = game.Game()
    dice = [1, 4, 4, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(3, dice) == old_score + 8


def calc_five_score_test():
    my_game = game.Game()
    dice = [5, 4, 4, 5, 5]
    old_score = my_game.score
    assert my_game.calc_score(4, dice) == old_score + 15


def calc_six_score_test():
    my_game = game.Game()
    dice = [6, 4, 4, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(5, dice) == old_score + 6


def calc_three_of_a_kind_score_test():
    my_game = game.Game()
    dice = [6, 4, 4, 4, 2]
    old_score = my_game.score
    assert my_game.calc_score(6, dice) == old_score + 20


def calc_four_of_a_kind_score_test():
    my_game = game.Game()
    dice = [6, 2, 2, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(7, dice) == old_score + 14


def calc_full_house_score_test():
    my_game = game.Game()
    dice = [2, 4, 4, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(8, dice) == old_score + 25


def calc_yahtzee_score_test():
    my_game = game.Game()
    dice = [2, 2, 2, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(11, dice) == old_score + 50


def calc_small_straight_score_test():
    my_game = game.Game()
    dice = [1, 2, 3, 4, 5]
    old_score = my_game.score
    assert my_game.calc_score(9, dice) == old_score + 30


def calc_large_straight_score_test():
    my_game = game.Game()
    dice = [1, 2, 3, 4, 5]
    old_score = my_game.score
    assert my_game.calc_score(10, dice) == old_score + 40


def calc_chance_score_test():
    my_game = game.Game()
    dice = [6, 4, 4, 6, 2]
    old_score = my_game.score
    assert my_game.calc_score(12, dice) == old_score + 22


def test_update_score_test():
    my_game = game.Game()
    old_score = my_game.score
    my_game.update_score(10, 0, 0)
    assert my_game.score == old_score + 10


def test_game_over_test():
    agent = AgentOne.ReRollGreedyAgent()
    for i in range(13):
        agent.do_turn()
    assert agent.my_game.game_over()


def test_greedy_agent_best_category():
    """this test checks if the greedy agent chooses the best category"""
    agent = AgentOne.GreedyAgent()
    agent.my_game.curr_state.dice = [6, 4, 4, 6, 2]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses chance
    assert agent.my_game.curr_state.categories[
               12] and agent.my_game.score == old_score + 22 and max_category == 12

    agent.my_game.curr_state.dice = [6, 6, 6, 6, 2]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses sixs
    assert agent.my_game.curr_state.categories[
               6] and agent.my_game.score == old_score + 26 and max_category == 6

    agent.my_game.curr_state.dice = [1, 1, 1, 1, 1]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses yahtzee
    assert agent.my_game.curr_state.categories[
               11] and agent.my_game.score == old_score + 50 and max_category == 11

    agent.my_game.curr_state.dice = [3, 3, 3, 1, 1]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses full house
    assert agent.my_game.curr_state.categories[
               8] and agent.my_game.score == old_score + 25 and max_category == 8


def test_greedy_straight():
    """ checks if the greedy agent takes the large straight over the small one"""
    agent = AgentOne.GreedyAgent()
    agent.my_game.curr_state.dice = [1, 2, 4, 3, 5]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    assert agent.my_game.curr_state.categories[
               10] and agent.my_game.score == old_score + 40 and max_category == 10


def test_random_agent():
    """ checks that the random agent works"""
    agent = AgentOne.RandomAgent()
    chosen_category = []
    for i in range(13):
        max_category, max_score, max_dice_roll = agent.do_turn()
        assert sum(agent.my_game.curr_state.categories) == i + 1 and max_category not in chosen_category
        chosen_category.append(max_category)


def test_expect_agent_no_re_rolls():
    agent = AgentOne.ExpectIMaxAgent()
    agent.my_game.curr_state.dice = [3, 3, 3, 2, 2]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to take full house
    assert agent.my_game.curr_state.categories[8] and chosen_category == 8

    agent.my_game.curr_state.dice = [1, 1, 1, 1, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to ones
    assert agent.my_game.curr_state.categories[0] and chosen_category == 0

    agent.my_game.curr_state.dice = [6, 6, 1, 1, 2]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to take chance
    assert agent.my_game.curr_state.categories[12] and chosen_category == 12

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to two's
    assert agent.my_game.curr_state.categories[1] and chosen_category == 1

    agent.my_game.curr_state.dice = [6, 6, 6, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to take 4 of a kind
    assert agent.my_game.curr_state.categories[7] and chosen_category == 7

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to two's
    assert agent.my_game.curr_state.categories[1] and chosen_category == 1


def test_expect_agent_with_re_rolls():
    agent = AgentOne.ExpectIMaxAgent()
    agent.my_game.curr_state.dice = [2, 2, 2, 2, 2]
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses yahtzee
    assert agent.my_game.curr_state.categories[11] and chosen_category == 11

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses tow's or yahtzee
    assert agent.my_game.curr_state.categories[8] and chosen_category == 8 or agent.my_game.curr_state.categories[
        11] and chosen_category == 11

    agent.my_game.curr_state.dice = [1, 1, 1, 2, 6]
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses one's or yahtzee or full house
    assert agent.my_game.curr_state.categories[0] and chosen_category == 0 or agent.my_game.curr_state.categories[
        11] and chosen_category == 11 or agent.my_game.curr_state.categories[8] and chosen_category == 8


def test_expect_agent_basic():
    agent = AgentOne.ExpectIMaxAgent()
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    assert agent.my_game.curr_state.categories[max_category] and agent.my_game.score == old_score + max_score


def test_random_greedy_n0_re_roll():
    agent = AgentOne.ReRollGreedyAgent()
    agent.my_game.curr_state.dice = [2, 2, 2, 2, 2]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses yahtzee
    assert agent.my_game.curr_state.categories[11] and chosen_category == 11

    agent.my_game.curr_state.dice = [2, 2, 1, 1, 1]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses full house
    assert agent.my_game.curr_state.categories[8] and chosen_category == 8

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses tow's
    assert agent.my_game.curr_state.categories[1] and chosen_category == 1



if __name__ == '__main__':
    test_random_agent()
import pytest
import game
import AgentOne
import state


def test_calc_scores():
    calc_one_score_test()
    calc_two_score_test()
    calc_three_score_test()
    calc_four_score_test()
    calc_five_score_test()
    calc_six_score_test()
    calc_large_straight_score_test()
    calc_small_straight_score_test()
    calc_full_house_score_test()
    calc_yahtzee_score_test()
    calc_chance_score_test()
    calc_three_of_a_kind_score_test()
    calc_four_of_a_kind_score_test()


def calc_two_score_test():
    my_game = game.Game()
    dice = [1, 1, 1, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(1, dice) == old_score + 4


def calc_one_score_test():
    my_game = game.Game()
    dice = [1, 1, 1, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(0, dice) == old_score + 3


def calc_three_score_test():
    my_game = game.Game()
    dice = [1, 3, 3, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(2, dice) == old_score + 6


def calc_four_score_test():
    my_game = game.Game()
    dice = [1, 4, 4, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(3, dice) == old_score + 8


def calc_five_score_test():
    my_game = game.Game()
    dice = [5, 4, 4, 5, 5]
    old_score = my_game.score
    assert my_game.calc_score(4, dice) == old_score + 15


def calc_six_score_test():
    my_game = game.Game()
    dice = [6, 4, 4, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(5, dice) == old_score + 6


def calc_three_of_a_kind_score_test():
    my_game = game.Game()
    dice = [6, 4, 4, 4, 2]
    old_score = my_game.score
    assert my_game.calc_score(6, dice) == old_score + 20


def calc_four_of_a_kind_score_test():
    my_game = game.Game()
    dice = [6, 2, 2, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(7, dice) == old_score + 14


def calc_full_house_score_test():
    my_game = game.Game()
    dice = [2, 4, 4, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(8, dice) == old_score + 25


def calc_yahtzee_score_test():
    my_game = game.Game()
    dice = [2, 2, 2, 2, 2]
    old_score = my_game.score
    assert my_game.calc_score(11, dice) == old_score + 50


def calc_small_straight_score_test():
    my_game = game.Game()
    dice = [1, 2, 3, 4, 5]
    old_score = my_game.score
    assert my_game.calc_score(9, dice) == old_score + 30


def calc_large_straight_score_test():
    my_game = game.Game()
    dice = [1, 2, 3, 4, 5]
    old_score = my_game.score
    assert my_game.calc_score(10, dice) == old_score + 40


def calc_chance_score_test():
    my_game = game.Game()
    dice = [6, 4, 4, 6, 2]
    old_score = my_game.score
    assert my_game.calc_score(12, dice) == old_score + 22


def test_update_score_test():
    my_game = game.Game()
    old_score = my_game.score
    my_game.update_score(10, 0, 0)
    assert my_game.score == old_score + 10


def test_game_over_test():
    agent = AgentOne.ReRollGreedyAgent()
    for i in range(13):
        agent.do_turn()
    assert agent.my_game.game_over()


def test_greedy_agent_best_category():
    """this test checks if the greedy agent chooses the best category"""
    agent = AgentOne.GreedyAgent()
    agent.my_game.curr_state.dice = [6, 4, 4, 6, 2]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses chance
    assert agent.my_game.curr_state.categories[
               12] and agent.my_game.score == old_score + 22 and max_category == 12

    agent.my_game.curr_state.dice = [6, 6, 6, 6, 2]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses sixs
    assert agent.my_game.curr_state.categories[
               6] and agent.my_game.score == old_score + 26 and max_category == 6

    agent.my_game.curr_state.dice = [1, 1, 1, 1, 1]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses yahtzee
    assert agent.my_game.curr_state.categories[
               11] and agent.my_game.score == old_score + 50 and max_category == 11

    agent.my_game.curr_state.dice = [3, 3, 3, 1, 1]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    # chooses full house
    assert agent.my_game.curr_state.categories[
               8] and agent.my_game.score == old_score + 25 and max_category == 8


def test_greedy_straight():
    """ checks if the greedy agent takes the large straight over the small one"""
    agent = AgentOne.GreedyAgent()
    agent.my_game.curr_state.dice = [1, 2, 4, 3, 5]
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    assert agent.my_game.curr_state.categories[
               10] and agent.my_game.score == old_score + 40 and max_category == 10


def test_random_agent():
    """ checks that the random agent works"""
    agent = AgentOne.RandomAgent()
    chosen_category = []
    for i in range(13):
        max_category, max_score, max_dice_roll = agent.do_turn()
        assert sum(agent.my_game.curr_state.categories) == i + 1 and max_category not in chosen_category
        chosen_category.append(max_category)


def test_expect_agent_no_re_rolls():
    agent = AgentOne.ExpectIMaxAgent()
    agent.my_game.curr_state.dice = [3, 3, 3, 2, 2]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to take full house
    assert agent.my_game.curr_state.categories[8] and chosen_category == 8

    agent.my_game.curr_state.dice = [1, 1, 1, 1, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to ones
    assert agent.my_game.curr_state.categories[0] and chosen_category == 0

    agent.my_game.curr_state.dice = [6, 6, 1, 1, 2]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to take chance
    assert agent.my_game.curr_state.categories[12] and chosen_category == 12

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to two's
    assert agent.my_game.curr_state.categories[1] and chosen_category == 1

    agent.my_game.curr_state.dice = [6, 6, 6, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to take 4 of a kind
    assert agent.my_game.curr_state.categories[7] and chosen_category == 7

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # expected to two's
    assert agent.my_game.curr_state.categories[1] and chosen_category == 1


def test_expect_agent_with_re_rolls():
    agent = AgentOne.ExpectIMaxAgent()
    agent.my_game.curr_state.dice = [2, 2, 2, 2, 2]
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses yahtzee
    assert agent.my_game.curr_state.categories[11] and chosen_category == 11

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses tow's or yahtzee
    assert agent.my_game.curr_state.categories[8] and chosen_category == 8 or agent.my_game.curr_state.categories[
        11] and chosen_category == 11

    agent.my_game.curr_state.dice = [1, 1, 1, 2, 6]
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses one's or yahtzee or full house
    assert agent.my_game.curr_state.categories[0] and chosen_category == 0 or agent.my_game.curr_state.categories[
        11] and chosen_category == 11 or agent.my_game.curr_state.categories[8] and chosen_category == 8


def test_expect_agent_basic():
    agent = AgentOne.ExpectIMaxAgent()
    old_score = agent.my_game.score
    max_category, max_score, max_dice_roll = agent.do_turn()
    assert agent.my_game.curr_state.categories[max_category] and agent.my_game.score == old_score + max_score


def test_random_greedy_n0_re_roll():
    agent = AgentOne.ReRollGreedyAgent()
    agent.my_game.curr_state.dice = [2, 2, 2, 2, 2]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses yahtzee
    assert agent.my_game.curr_state.categories[11] and chosen_category == 11

    agent.my_game.curr_state.dice = [2, 2, 1, 1, 1]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses full house
    assert agent.my_game.curr_state.categories[8] and chosen_category == 8

    agent.my_game.curr_state.dice = [2, 2, 2, 2, 6]
    agent.my_game.curr_state.rerolls = 0
    chosen_category, max_score, max_dice_roll = agent.do_turn()
    # chooses tow's
    assert agent.my_game.curr_state.categories[1] and chosen_category == 1



if __name__ == '__main__':
    test_random_agent()
