from test_python_package_release import reverse_string, snake_to_camel


def test_reverse_string():
    assert reverse_string("abc") == "cba"


def test_reverse_string_empty():
    assert reverse_string("") == ""


def test_snake_to_camel():
    assert snake_to_camel("hello_world_foo") == "helloWorldFoo"


def test_snake_to_camel_single_word():
    assert snake_to_camel("single") == "single"
