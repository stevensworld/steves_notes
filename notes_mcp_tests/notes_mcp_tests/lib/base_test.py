import os
import tempfile
import unittest
from steves_notes import Builder
from note_iterator import NoteIterator
import notes_mcp.server as server_module


class BaseTest(unittest.TestCase):
    description = "no description provided"
    expected = "no expected value provided"

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        notes_path = os.path.join(self.tmpdir.name, "notes.json")
        self.builder = Builder(filename=notes_path)
        self.iterator = NoteIterator(self.builder.root)
        server_module.builder = self.builder
        server_module.iterator = self.iterator

    def tearDown(self):
        self.tmpdir.cleanup()

    def get_description(self):
        return self.description

    def get_expected(self):
        return self.expected
