import pytest

from test_python_package_release import (
    add,
    divide,
    is_divisible,
    modulo,
    multiply,
    power,
    sqrt,
    subtract,
)


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_power():
    assert power(2, 10) == 1024


def test_power_zero_exponent():
    assert power(5, 0) == 1


def test_power_negative_exponent():
    assert power(2, -2) == 0.25


def test_modulo():
    assert modulo(10, 3) == 1


def test_modulo_by_zero():
    with pytest.raises(ZeroDivisionError):
        modulo(5, 0)


def test_sqrt():
    assert sqrt(9) == 3.0


def test_sqrt_zero():
    assert sqrt(0) == 0.0


def test_sqrt_negative():
    with pytest.raises(ValueError):
        sqrt(-1)


def test_is_divisible_true():
    assert is_divisible(10, 2) is True


def test_is_divisible_false():
    assert is_divisible(10, 3) is False


def test_is_divisible_by_zero():
    with pytest.raises(ZeroDivisionError):
        is_divisible(5, 0)
