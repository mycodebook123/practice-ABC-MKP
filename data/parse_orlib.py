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