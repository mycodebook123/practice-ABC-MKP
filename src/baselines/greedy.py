from src.mkp.problem import item_scores, profit


def greedy(inst):
    # best score first, take an item only if it still fits
    # ties go to the lower index. returns (x, total profit)
    scores = item_scores(inst)
    order = sorted(range(inst.n), key=lambda j: (-scores[j], j))
    x = [0] * inst.n
    used = [0] * inst.m
    for j in order:
        fits = all(used[i] + inst.weights[i][j] <= inst.capacities[i]
                   for i in range(inst.m))
        if fits:
            x[j] = 1
            for i in range(inst.m):
                used[i] += inst.weights[i][j]
    return x, profit(inst, x)