import os
import tempfile
import unittest

from process_manager.state import ProcessState


class TestProcessState(unittest.TestCase):

    def test_write_and_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("test", 12345, ["python", "foo.py"])
            result = state.read("test")
            self.assertEqual(result["pid"], 12345)
            self.assertEqual(result["command"], ["python", "foo.py"])
            self.assertIn("started_at", result)

    def test_read_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            self.assertIsNone(state.read("nonexistent"))

    def test_clear_removes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("test", 12345, ["python", "foo.py"])
            state.clear("test")
            self.assertIsNone(state.read("test"))

    def test_clear_silent_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.clear("nonexistent")

    def test_all_names_returns_all(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("a", 1, [])
            state.write("b", 2, [])
            state.write("c", 3, [])
            self.assertCountEqual(state.all_names(), ["a", "b", "c"])

    def test_all_names_empty_when_no_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            self.assertEqual(state.all_names(), [])

    def test_read_returns_none_on_corrupt_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            with open(state.path("bad"), "w") as f:
                f.write("not valid json {{{")
            self.assertIsNone(state.read("bad"))
