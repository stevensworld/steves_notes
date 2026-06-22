import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateWriteAndRead(unittest.TestCase):

    def test_state_write_and_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)
            state.write("test", 12345, ["python", "foo.py"])
            result = state.read("test")

            print(f"\n  expected: pid=12345, command=['python', 'foo.py'], started_at present")
            print(f"  actual:   pid={result['pid']}, command={result['command']}, started_at={result.get('started_at')}")

            self.assertEqual(result["pid"], 12345)
            self.assertEqual(result["command"], ["python", "foo.py"])
            self.assertIn("started_at", result)
