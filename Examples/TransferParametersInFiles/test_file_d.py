# test_file_d.py     - this files will be handle by pytest
# RUN THIS FILE WITH PYTEST from the command line!!!!!!!!
# pip install pytest

# pytest is a testing framework that makes it easy to write simple and scalable test cases.
# pytest is a powerful testing framework for Python
# This is a built-in Python statement that checks if a condition is True. If not, it raises an AssertionError
# if assert passes, the test is successful. If it fails, it stops with an error.

from file_d import divide_numbers

#Assert conditions, "Optional error message" -> If the condition is True, the program continues normally.
def test_divide():
    assert divide_numbers(10, 2) == 5        # ✅ This is True, nothing happens
    assert divide_numbers(10, 0) is None     # ✅ This is True, nothing happens
    assert divide_numbers(10, 5) == 2        # ✅ This is True, nothing happens





    