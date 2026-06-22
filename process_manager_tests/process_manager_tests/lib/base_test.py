import os
import tempfile
import unittest

from process_manager import ProcessManager


class BaseTest(unittest.TestCase):

    description = "no description provided"
    expected = "no expected value provided"

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.pm = ProcessManager(pid_dir=os.path.join(self.tmpdir.name, "pids"))

    def tearDown(self):
        self.pm.stop_all()
        self.tmpdir.cleanup()

    def get_description(self):
        return self.description

    def get_expected(self):
        return self.expected
