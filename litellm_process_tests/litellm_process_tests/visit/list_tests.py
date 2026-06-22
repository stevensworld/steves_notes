import os
from test_utils.list_tests import list_tests

active_dir = os.path.join(os.path.dirname(__file__), "../active")

if __name__ == "__main__":
    for test in list_tests(active_dir):
        print(test)
