import re

from src.mkp.problem import Instance


def _clean(v):
    # 3800.0 -> 3800, but leave 8706.1 alone
    return int(v) if v == int(v) else v


def read_numbers(path):
    # rows wrap over several lines in these files, so just read every
    # number into one flat list and ignore the line structure
    with open(path) as f:
        return [float(tok) for tok in f.read().split()]


def parse_numbers(nums, prefix, first_index=1):
    # layout: count, then for each problem "n m optimum", n profits,
    # m rows of n weights, m capacities
    pos = 0
    count = int(nums[pos])
    pos += 1
    instances = []
    for k in range(count):
        n, m, opt = int(nums[pos]), int(nums[pos + 1]), nums[pos + 2]
        pos += 3
        profits = [_clean(v) for v in nums[pos:pos + n]]
        pos += n
        weights = []
        for _ in range(m):
            weights.append([_clean(v) for v in nums[pos:pos + n]])
            pos += n
        capacities = [_clean(v) for v in nums[pos:pos + m]]
        pos += m
        bks = _clean(opt) if opt != 0 else None  # 0 = optimum not known
        instances.append(Instance(f"{prefix}-{k + first_index}", n, m,
                                  profits, weights, capacities, bks))
    if pos != len(nums):
        raise ValueError(f"{len(nums) - pos} numbers left over, wrong layout?")
    return instances


def load_orlib(path, prefix, first_index=1):
    return parse_numbers(read_numbers(path), prefix, first_index)


def load_mkcbres(path):
    # mkcbres.txt has two tables of lines like "5.100-00   24381".
    # first table is the best feasible value, second is the LP relaxation,
    # so the first time a name shows up it's the best value and the second
    # time it's the LP value. returns (best, lp) as two dicts
    best, lp = {}, {}
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and re.fullmatch(r"\d+\.\d+-\d+", parts[0]):
                value = _clean(float(parts[1]))
                if parts[0] not in best:
                    best[parts[0]] = value
                else:
                    lp[parts[0]] = value
    return best, lp


def load_mknapcb(path, results_path, prefix):
    # load one mknapcb file and fill in bks from mkcbres.txt
    # the key is built from the instance: "<m>.<n>-<index>", like 5.100-00
    instances = load_orlib(path, prefix, first_index=0)
    best, _ = load_mkcbres(results_path)
    for k, inst in enumerate(instances):
        inst.bks = best[f"{inst.m}.{inst.n}-{k:02d}"]
    return instances