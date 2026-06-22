import tempfile
import unittest
from process_manager.state import ProcessState


class TestStateClearSilentWhenMissing(unittest.TestCase):

    def test_state_clear_silent_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state = ProcessState(tmpdir)

            print(f"\n  expected: no exception raised when clearing nonexistent entry")

            try:
                state.clear("nonexistent")
                print(f"  actual:   no exception raised")
            except Exception as e:
                print(f"  actual:   exception raised: {e}")
                raise
