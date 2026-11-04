from src.mkp.problem import Instance, get_toy_instances, is_feasible
from src.baselines.greedy import greedy

# mknap1 problem 1: 6 items, 10 constraints, optimum 3800
MKNAP1_P1 = Instance(
    "mknap1-1", 6, 10,
    [100, 600, 1200, 2400, 500, 2000],
    [[8, 12, 13, 64, 22, 41],
     [8, 12, 13, 75, 22, 41],
     [3, 6, 4, 18, 6, 4],
     [5, 10, 8, 32, 6, 12],
     [5, 13, 8, 42, 6, 20],
     [5, 13, 8, 48, 6, 20],
     [0, 0, 0, 0, 8, 0],
     [3, 0, 4, 0, 8, 0],
     [3, 2, 4, 0, 8, 4],
     [3, 2, 4, 8, 8, 4]],
    [80, 96, 20, 36, 44, 48, 10, 18, 22, 24],
    bks=3800)


def test_greedy_finds_optimum_on_mknap1_problem1():
    x, value = greedy(MKNAP1_P1)
    assert x == [0, 1, 1, 0, 0, 1]
    assert value == 3800


def test_greedy_result_is_always_feasible():
    for inst in get_toy_instances() + [MKNAP1_P1]:
        x, _ = greedy(inst)
        assert is_feasible(inst, x)


def test_greedy_gives_same_answer_every_time():
    assert greedy(MKNAP1_P1) == greedy(MKNAP1_P1)