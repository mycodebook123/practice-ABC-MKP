import os
import pytest
from data.parse_orlib import load_mkcbres, load_mknapcb

# tiny stand-in for mkcbres.txt: two tables, the first value is the best
# feasible one, the second is the LP value
RESULTS = """The first table given below gives the best feasible solution value.

Problem Name        Best Feasible Solution Value

1.3-00                  7
1.3-01                  9

The second table gives the LP relaxation.

Problem Name        LP value

1.3-00                  7.5
1.3-01                  9.25
"""

# two problems with 3 items and 1 constraint (optimum field is 0)
PROBLEMS = """2
3 1 0
5 4 3
4 3 2
5
3 1 0
6 5 4
2 2 2
5
"""


def test_mkcbres_two_tables(tmp_path):
    f = tmp_path / "res.txt"
    f.write_text(RESULTS)
    best, lp = load_mkcbres(str(f))
    assert best == {"1.3-00": 7, "1.3-01": 9}
    assert lp == {"1.3-00": 7.5, "1.3-01": 9.25}


def test_mknapcb_gets_reference_values(tmp_path):
    res = tmp_path / "res.txt"
    res.write_text(RESULTS)
    prob = tmp_path / "cb.txt"
    prob.write_text(PROBLEMS)
    insts = load_mknapcb(str(prob), str(res), "mknapcb-test")
    assert [i.name for i in insts] == ["mknapcb-test-0", "mknapcb-test-1"]
    assert [i.bks for i in insts] == [7, 9]


CB = {k: os.path.join("data", "raw", f"mknapcb{k}.txt") for k in (1, 2, 3)}
RES = os.path.join("data", "raw", "mkcbres.txt")
HAVE_FILES = all(os.path.exists(p) for p in [RES] + list(CB.values()))


@pytest.mark.skipif(not HAVE_FILES, reason="OR-Library files not downloaded")
def test_real_mknapcb_files():
    cb1 = load_mknapcb(CB[1], RES, "mknapcb1")
    assert len(cb1) == 30
    assert (cb1[0].n, cb1[0].m) == (100, 5)
    assert [i.bks for i in cb1[:5]] == [24381, 24274, 23551, 23534, 23991]
    cb2 = load_mknapcb(CB[2], RES, "mknapcb2")
    cb3 = load_mknapcb(CB[3], RES, "mknapcb3")
    assert (cb2[0].n, cb2[0].m) == (250, 5)
    assert (cb3[0].n, cb3[0].m) == (500, 5)