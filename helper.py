from pprint import pprint

"""Helper method to test functions"""

def ut(callable, *args):
    ut.call_count +=1
    print("---------------")
    print(f"N°{ut.call_count} - Testing {callable.__name__}")
    print("---------------")
    ret = callable(*args)
    pprint(ret)

    ## new lines
    print()
    print()
    return ret
ut.call_count = 0