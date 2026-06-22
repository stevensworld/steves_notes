import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateAllNamesReturnsAll(unittest.TestCase):

    def test_state_all_names_returns_all(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("a", 1, [])
            state.write("b", 2, [])
            state.write("c", 3, [])
            result = state.all_names()

            print(f"\n  expected: ['a', 'b', 'c'] (any order)")
            print(f"  actual:   {sorted(result)}")

            self.assertCountEqual(result, ["a", "b", "c"])
