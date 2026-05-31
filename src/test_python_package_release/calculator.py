def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float) -> float:
    return base**exponent


def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero")
    return a % b


def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("Cannot take square root of a negative number")
    return x**0.5


def is_divisible(a: float, b: float) -> bool:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a % b == 0
