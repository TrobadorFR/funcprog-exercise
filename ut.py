"""File: ut.py
Houses any functions used as helpers for unit testing."""

from pprint import *


def ut_print(callable, *args):
    """Helper method to test functions"""
    ut_print.call_count +=1
    print("---------------")
    print(f"N°{ut_print.call_count} - Testing {callable.__name__}")
    print("---------------")
    ret = callable(*args)
    pprint(ret)

    ## new lines
    print()
    print()
    return ret
ut_print.call_count = 0


def ut_repr(callable, *args):
    """Helper method to test functions"""
    print("---------------")
    print(f"Testing {callable.__name__}")
    print("---------------")
    ret = callable(*args)
    return pformat(ret)

