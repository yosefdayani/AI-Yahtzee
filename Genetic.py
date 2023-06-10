import ExpectiMaxAgent
import numpy as np
import game

MUTATE_PROB = 0.6
COORD_PROB = 0.6
REP = 40
THROWS = [0.7,0.3,0.03,0.01,0,0,0.02,0.04,0,0,0.15,0.6,0.02]
AVGS = [15,13,10,13,14.99,19,25,24,25,40,20,5,30]
AVGS_POP = [AVGS, [0.5 * a for a in AVGS], [1.5 * a for a in AVGS]
    , [a + 0.4 for a in AVGS], [a - 0.4 for a in AVGS], [1.2 * a for a in AVGS]]
N_POP = len(AVGS_POP)
THROWS_POP = [THROWS, [0.5 * t for t in THROWS], [1.5 * t for t in THROWS],
              [1.2 * t for t in THROWS],
              [t + 0.4 for t in THROWS], [t - 0.4 for t in THROWS]]


def produce(p1, p2):
    """
    creates new individual from the given parents, p1 and p2 as described in the PDF.
    """
    return [(p1[i] + p2[i]) / 2 for i in range(len(p1))]


def mutate(individual):
    """
    mutation of the new individual (described in the PDF)
    :param individual:
    :return:
    """
    coordinates = [True if k < COORD_PROB else False for k in np.random.rand(13)]
    return [coord + 2 * (np.random.rand() - 0.5) if coordinates[i] else coord for i, coord in
            enumerate(individual)]


def prob_vec(size):
    """
    probability vectors for multinomial choice of the parents.
    :param size:
    :return:
    """
    if size == 5:
        return [0.5, 0.2, 0.12, 0.1, 0.08]
    return [0.4, 0.3, 0.2, 0.1]


def run_game(agent):
    """
    run single game of a given agent and returns the score.
    """
    while not agent.my_game.game_over():
        agent.do_turn()
    score = agent.my_game.score
    agent.my_game = game.Game()
    return score


def run_games(agent):
    """
    run REP games of the given agent and return the scores.
    """
    return np.array([run_game(agent) for i in range(REP)])


def genetic_init(pop, indicator_avgs):
    """
    initialization for the genetic algorithm
    """
    pop_score = np.zeros((N_POP, REP))
    for i in range(pop_score.shape[0]):
        print("here")
        if indicator_avgs:
            agent = ExpectiMaxAgent.ExpectiMaxAgent(pop[i], THROWS)
        else:
            agent = ExpectiMaxAgent.ExpectiMaxAgent(AVGS, pop[i])
        pop_score[i] = run_games(agent)
    means = np.apply_along_axis(aggregate, 1, pop_score)
    arg_sort = np.argsort(means)[::-1]
    sorted_pop = [pop[arg] for arg in arg_sort]
    means = sorted(means, reverse=True)
    return sorted_pop, means


def aggregate(score_vec):
    """
    aggregation of the agent performance (average score)
    :param score_vec:
    :return:
    """
    return np.mean(score_vec)


def choose_parents(pop):
    """
    choose the parents of the new individual, higher probabilities for better individuals
    :param pop: population
    :return:
    """
    father_ind = np.random.multinomial(1, prob_vec(5)).argmax()
    mother_ind = np.random.multinomial(1, prob_vec(4)).argmax()
    pop_copy = pop.copy()
    pop_copy.pop(father_ind)
    return pop[father_ind], pop_copy[mother_ind]


def genetic(pop, avgs_indicator, reps):
    """
    genetic algorithm to find the best W,T vectors described in the PDF.
    :param pop: population
    :param avgs_indicator: true if finding W, else finding T
    :param reps: number of iterations
    """
    pop, means = genetic_init(pop, avgs_indicator)
    for i in range(reps):
        print("in", "\n------------\n", pop, means)
        father, mother = choose_parents(pop)
        pop[-1] = produce(father, mother)
        if avgs_indicator:
            new_agent = ExpectiMaxAgent.ExpectiMaxAgent(pop[-1], THROWS)
        else:
            new_agent = ExpectiMaxAgent.ExpectiMaxAgent(AVGS, pop[-1])
        means[-1] = aggregate(run_games(new_agent))
        arg_sort = np.argsort(means)[::-1]
        sorted_pop = [pop[arg] for arg in arg_sort]
        pop = sorted_pop
        means = sorted(means, reverse=True)
    return pop, means


# avgs,throws= AVGS_POP,THROWS_POP
# for i in range(200):
#     avgs,avgs_means =genetic(avgs,avgs_indicator=True,reps=5) # 5 for W
#     throws, throws_means = genetic(throws,avgs_indicator= False,reps=  5) # 5 for T
#


