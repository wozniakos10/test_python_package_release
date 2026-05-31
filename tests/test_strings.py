from test_python_package_release import (
    camel_to_snake,
    count_words,
    reverse_string,
    snake_to_camel,
    truncate,
)


def test_reverse_string():
    assert reverse_string("abc") == "cba"


def test_reverse_string_empty():
    assert reverse_string("") == ""


def test_snake_to_camel():
    assert snake_to_camel("hello_world_foo") == "helloWorldFoo"


def test_snake_to_camel_single_word():
    assert snake_to_camel("single") == "single"


def test_count_words():
    assert count_words("hello world foo") == 3


def test_count_words_empty():
    assert count_words("") == 0


def test_count_words_whitespace_only():
    assert count_words("   ") == 0


def test_camel_to_snake():
    assert camel_to_snake("helloWorldFoo") == "hello_world_foo"


def test_camel_to_snake_single_word():
    assert camel_to_snake("hello") == "hello"


def test_truncate_short():
    assert truncate("hello", 10) == "hello"


def test_truncate_exact():
    assert truncate("hello", 5) == "hello"


def test_truncate_long():
    assert truncate("hello world", 8) == "hello..."


def test_truncate_custom_suffix():
    assert truncate("hello world", 7, suffix="!") == "hello !"
