import importlib.util
import os
import sys
import unittest

TEST_PACKAGES = {
    "process_manager_tests": [
        "test_state_write_and_read",
        "test_state_read_missing",
        "test_state_clear_removes_file",
        "test_state_clear_silent_when_missing",
        "test_state_all_names_returns_all",
        "test_state_all_names_empty",
        "test_state_read_corrupt_file",
        "test_start_returns_true",
        "test_start_writes_state",
        "test_start_process_is_alive",
        "test_start_already_running_no_restart",
        "test_start_ready_fn_true_immediately",
        "test_start_ready_fn_timeout",
        "test_stop_kills_process",
        "test_stop_clears_state",
        "test_stop_unknown_is_silent",
        "test_stop_already_dead_is_silent",
        "test_restart_gives_new_pid",
        "test_restart_process_alive_after",
        "test_restart_raises_if_never_started",
        "test_status_running",
        "test_status_not_running",
        "test_status_after_stop",
        "test_stop_all_stops_multiple",
        "test_stop_all_empty_is_silent",
        "test_persistence_readable_by_new_instance",
        "test_persistence_stop_by_new_instance",
    ],
}


def load_module(package_name, module_name, active_dir):
    path = os.path.join(active_dir, f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_active_dir(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        raise ImportError(f"{package_name} is not installed")
    return os.path.join(os.path.dirname(spec.origin), "active")


def run():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for package_name, modules in TEST_PACKAGES.items():
        active_dir = find_active_dir(package_name)
        for module_name in modules:
            module = load_module(package_name, module_name, active_dir)
            suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run()
