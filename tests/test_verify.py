from src.mkp.problem import Instance, get_toy_instances
from data.verify_bks import brute_force_best


def test_brute_force_matches_toy_values():
    for toy in get_toy_instances():
        assert brute_force_best(toy) == toy.bks


def test_brute_force_handles_decimal_profits():
    # only one of the two items fits, the better one is worth 2.5
    inst = Instance("dec", 2, 1, [1.5, 2.5], [[1, 1]], [1], bks=2.5)
    assert abs(brute_force_best(inst) - 2.5) < 1e-9