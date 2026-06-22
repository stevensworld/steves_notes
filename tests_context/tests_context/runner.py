import importlib.util
import os
import sys
import unittest

TEST_PACKAGES = [
    "process_manager_tests",
]


def find_active_dir(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        raise ImportError(f"{package_name} is not installed")
    package_dir = os.path.dirname(spec.origin)
    active_dir = os.path.join(package_dir, "active")
    if not os.path.isdir(active_dir):
        raise FileNotFoundError(f"No active/ directory found in {package_dir}")
    return active_dir


def run():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for package_name in TEST_PACKAGES:
        active_dir = find_active_dir(package_name)
        discovered = loader.discover(start_dir=active_dir, pattern="test_*.py")
        suite.addTests(discovered)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run()
