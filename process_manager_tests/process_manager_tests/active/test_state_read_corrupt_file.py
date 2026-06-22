import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateReadCorruptFile(unittest.TestCase):

    def test_state_read_corrupt_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            with open(state.path("bad"), "w") as f:
                f.write("not valid json {{{")
            result = state.read("bad")

            print(f"\n  expected: None on corrupt file")
            print(f"  actual:   {result}")

            self.assertIsNone(result)
