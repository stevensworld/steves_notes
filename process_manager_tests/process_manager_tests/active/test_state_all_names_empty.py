import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateAllNamesEmpty(unittest.TestCase):

    def test_state_all_names_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            result = state.all_names()

            print(f"\n  expected: []")
            print(f"  actual:   {result}")

            self.assertEqual(result, [])
