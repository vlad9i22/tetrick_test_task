from solution import strict
import pytest


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


def test_simple():
    assert sum_two(4, 5) == 9


def test_wrong_type():
    a_values = [True, False, "dsf", "", 23]
    b_values = [2, 5, 55, 1, 4.5]
    for a, b in zip(a_values, b_values):
        with pytest.raises(TypeError):
            sum_two(a, b)


@strict
def make_string(a: int, b: str, r: bool, e: float) -> str:
    return str(a) + str(b) + str(r) + str(e)


def test_mutiple_vars():
    assert make_string(1, "23", True, 4.1) == "123True4.1"


@strict
def no_annotations(a, b: int) -> int:
    return None


def test_bad_annotations():
    with pytest.raises(TypeError):
        no_annotations(1, 2)
