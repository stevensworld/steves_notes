import importlib.util
import os
import sys
import time
import unittest

from test_utils.list_tests import list_tests


def load_test_module(filename, active_dir):
    path = os.path.join(active_dir, filename)
    module_name = filename[:-3]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_test_class(module):
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase) and obj.__name__ != "BaseTest":
            return obj
    return None


def run(active_dir):
    passed = 0
    failed = 0

    for filename in list_tests(active_dir):
        print(f"Loading test: {filename}")
        module = load_test_module(filename, active_dir)
        cls = find_test_class(module)
        if cls is None:
            continue

        instance = cls()
        print(f"\tdescription: {instance.get_description()}")
        expected = instance.get_expected()

        test_methods = [m for m in dir(cls) if m.startswith("test_")]
        for method_name in test_methods:
            print(f"\trunning test: {method_name}")
            suite = unittest.TestLoader().loadTestsFromName(method_name, cls)
            result = unittest.TestResult()
            start = time.time()
            suite.run(result)
            elapsed = time.time() - start

            if result.wasSuccessful():
                print(f"PASS  {cls.__name__}.{method_name} ({elapsed:.3f}s)")
                print(f"      expected: {expected}")
                passed += 1
            else:
                print(f"FAIL  {cls.__name__}.{method_name} ({elapsed:.3f}s)")
                print(f"      expected: {expected}")
                for _, traceback in result.failures + result.errors:
                    print(f"      {traceback.strip().splitlines()[-1]}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
