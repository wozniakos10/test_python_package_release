import pytest

from test_python_package_release import add, divide, multiply, power, subtract


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
