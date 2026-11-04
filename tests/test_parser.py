import os
import pytest
from data.parse_orlib import load_orlib, parse_numbers

# two tiny problems, lines wrapped like the real files
# problem 1: 3 items, 2 constraints, optimum 15
# problem 2: 2 items, 1 constraint, optimum 0 (means unknown)
SAMPLE = """2
3 2 15
10 20
30
1 2 3
4 5
6
100 200
2 1 0
5 7
3 1
4
"""


def test_parser_reads_wrapped_numbers(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text(SAMPLE)
    insts = load_orlib(str(f), "sample")
    assert len(insts) == 2
    first, second = insts
    assert (first.n, first.m, first.bks) == (3, 2, 15)
    assert first.profits == [10, 20, 30]
    assert first.weights == [[1, 2, 3], [4, 5, 6]]
    assert first.capacities == [100, 200]
    assert first.name == "sample-1"
    assert (second.n, second.m) == (2, 1)
    assert second.weights == [[3, 1]]
    assert second.capacities == [4]
    assert second.bks is None


def test_parser_complains_about_leftovers():
    # one problem (1 item, 1 constraint) plus two stray numbers
    with pytest.raises(ValueError):
        parse_numbers([1, 1, 1, 0, 5, 3, 2, 99, 99], "x")


REAL = os.path.join("data", "raw", "mknap1.txt")


@pytest.mark.skipif(not os.path.exists(REAL), reason="mknap1.txt not downloaded")
def test_real_mknap1():
    insts = load_orlib(REAL, "mknap1")
    assert [(i.n, i.m) for i in insts] == [(6, 10), (10, 10), (15, 10), (20, 10),
                                           (28, 10), (39, 5), (50, 5)]
    assert [i.bks for i in insts] == [3800, 8706.1, 4015, 6120, 12400, 10618, 16537]