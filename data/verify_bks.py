import csv
import numpy as np

from data.parse_orlib import load_orlib


def brute_force_best(inst):
    # tries every selection, so only OK for small n (2**n of them, n <= 22 or so)
    # profits can be decimals (mknap1 problem 2), hence floats everywhere
    n = inst.n
    masks = np.arange(2 ** n, dtype=np.int64)
    # one row per selection, column j is 1 if item j is taken
    x = ((masks[:, None] >> np.arange(n)) & 1).astype(np.float64)
    weights = np.array(inst.weights, dtype=np.float64)    # m x n
    used = x @ weights.T                                   # (2**n) x m
    ok = (used <= np.array(inst.capacities, dtype=np.float64) + 1e-9).all(axis=1)
    profits = x @ np.array(inst.profits, dtype=np.float64)
    return float(profits[ok].max())


def verify_file(path, prefix, out_csv, max_n=22):
    rows = []
    for inst in load_orlib(path, prefix):
        if inst.n > max_n:
            rows.append([inst.name, inst.n, inst.m, inst.bks, "", "too large"])
            continue
        best = round(brute_force_best(inst), 6)
        status = "match" if abs(best - inst.bks) < 1e-6 else "DIFFERENT"
        rows.append([inst.name, inst.n, inst.m, inst.bks, best, status])
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instance", "n", "m", "published_optimum", "brute_force", "status"])
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    for r in verify_file("data/raw/mknap1.txt", "mknap1", "data/bks_verification.csv"):
        print(r)