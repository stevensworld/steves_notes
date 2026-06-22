import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateClearRemovesFile(unittest.TestCase):

    def test_state_clear_removes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("test", 12345, ["python", "foo.py"])
            state.clear("test")
            result = state.read("test")

            print(f"\n  expected: None after clear")
            print(f"  actual:   {result}")

            self.assertIsNone(result)
