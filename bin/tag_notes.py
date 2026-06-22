#!/usr/bin/env python3
import os
import sys
from audio_tagger import AudioTagger

notes_file = sys.argv[1] if len(sys.argv) > 1 else "notes.json"
mp3_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/speak_notes/mp3"

AudioTagger(notes_file=notes_file, mp3_dir=mp3_dir).run()
