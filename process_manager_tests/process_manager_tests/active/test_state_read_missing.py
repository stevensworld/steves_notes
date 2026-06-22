import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateReadMissing(unittest.TestCase):

    def test_state_read_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            result = state.read("nonexistent")

            print(f"\n  expected: None")
            print(f"  actual:   {result}")

            self.assertIsNone(result)
