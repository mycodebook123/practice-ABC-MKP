from src.mkp.problem import (get_toy_instances, profit, usage,
                             is_feasible, item_scores)


def test_toy1_profit_and_usage():
    toy1 = get_toy_instances()[0]
    assert profit(toy1, [1, 0, 0, 1]) == 14
    assert usage(toy1, [1, 0, 0, 1]) == [8, 8]


def test_using_exactly_the_capacity_is_feasible():
    toy1 = get_toy_instances()[0]
    assert is_feasible(toy1, [1, 0, 0, 1])  # 8 of 8 on the second resource


def test_everything_breaks_toy1():
    toy1 = get_toy_instances()[0]
    assert not is_feasible(toy1, [1, 1, 1, 1])


def test_empty_selection():
    for inst in get_toy_instances():
        x = [0] * inst.n
        assert profit(inst, x) == 0
        assert is_feasible(inst, x)


def test_toy3_everything_fits():
    toy3 = get_toy_instances()[2]
    assert is_feasible(toy3, [1, 1, 1])
    assert profit(toy3, [1, 1, 1]) == 6


def test_scores_toy1():
    scores = item_scores(get_toy_instances()[0])
    assert round(scores[0], 2) == 8.16
    assert round(scores[3], 2) == 6.96


def test_best_value_matches_brute_force():
    # try every selection, compare with the bks in the toy
    for inst in get_toy_instances():
        best = 0
        for mask in range(2 ** inst.n):
            x = [(mask >> j) & 1 for j in range(inst.n)]
            if is_feasible(inst, x):
                best = max(best, profit(inst, x))
        assert best == inst.bks