from dataclasses import dataclass


@dataclass
class Instance:
    name: str
    n: int              # items
    m: int              # constraints
    profits: list       # length n
    weights: list       # weights[i][j] = how much of resource i item j uses
    capacities: list    # length m
    bks: float = None   # best known value, None if we don't have one


def profit(inst, x):
    # x is a 0/1 list, one entry per item
    return sum(p for p, bit in zip(inst.profits, x) if bit)


def usage(inst, x):
    # how much of each resource x uses
    return [
        sum(inst.weights[i][j] for j in range(inst.n) if x[j])
        for i in range(inst.m)
    ]


def is_feasible(inst, x):
    # using exactly the capacity is fine
    return all(u <= c for u, c in zip(usage(inst, x), inst.capacities))


def item_scores(inst):
    # profit divided by the item's total share of all capacities.
    # items that use nothing get inf
    scores = []
    for j in range(inst.n):
        share = sum(inst.weights[i][j] / inst.capacities[i] for i in range(inst.m))
        scores.append(inst.profits[j] / share if share > 0 else float("inf"))
    return scores


def get_toy_instances():
    # small cases, best answers worked out by hand
    toy1 = Instance("toy1", 4, 2,
                    [10, 7, 6, 4],
                    [[6, 4, 5, 2], [5, 4, 2, 3]],
                    [10, 8], bks=14)
    toy2 = Instance("toy2", 3, 1,
                    [5, 4, 3],
                    [[4, 3, 2]],
                    [5], bks=7)
    toy3 = Instance("toy3", 3, 2,
                    [3, 2, 1],
                    [[1, 1, 1], [2, 1, 1]],
                    [3, 4], bks=6)  # everything fits
    return [toy1, toy2, toy3]