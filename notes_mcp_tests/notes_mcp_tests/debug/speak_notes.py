import asyncio
import json
import os
import re
import shutil
from fastmcp import Client
from notes_mcp.server import mcp
from kokoro_client import KokoroClient
from audio_tagger import AudioTagger

OUTPUT_DIR = "/tmp/speak_notes"
DEST = "/tmp/speak_notes/mp3"
NOTES_FILE = "notes.json"

kokoro = KokoroClient()


async def main():
    async with Client(mcp) as client:
        await client.call_tool("new_iterator")
        count = 0
        while True:
            result = await client.call_tool("get_next_note")
            text = result.content[0].text if result.content else ""
            if "All" in text and "visited" in text:
                print(f"\n── Done. {count} notes spoken.")
                break
            note = json.loads(text)
            node_id = note.get("node_id", f"note_{count:05}")
            note_text = note.get("text", "") or note.get("metadata", {}).get("text_content", "")
            if not note_text.strip():
                continue
            count += 1
            print(f"── [{node_id}] {note.get('name', '')} — generating audio...")
            path = kokoro.speak(note_text, name=node_id, output_dir=OUTPUT_DIR, dest=DEST)
            print(f"   saved: {path}")
            AudioTagger(notes_file=NOTES_FILE, mp3_dir=DEST).tag_note(node_id)

        playlist = os.path.join(DEST, "playlist.m3u")
        files = sorted([f for f in os.listdir(DEST) if f.endswith(".mp3")])
        with open(playlist, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for mp3 in files:
                f.write(f"{mp3}\n")
        print(f"── Playlist written: {playlist}")

        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            module_data = json.load(f)

        def to_folder_name(s):
            return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')

        module_name = to_folder_name(module_data.get("name", "module"))
        objectives = [c for c in module_data.get("children", []) if c.get("type") == "objective"]
        obj_name = to_folder_name(objectives[-1].get("name", "objective")) if objectives else "objective"

        speak_dir = os.path.join(os.path.expanduser("~/speak"), module_name, obj_name)
        os.makedirs(speak_dir, exist_ok=True)

        for mp3 in files:
            shutil.copy(os.path.join(DEST, mp3), os.path.join(speak_dir, mp3))
        shutil.copy(playlist, os.path.join(speak_dir, "playlist.m3u"))
        print(f"── Copied to: {speak_dir}")
        print(f"\n── Done. {count} notes spoken and tagged.")


if __name__ == "__main__":
    asyncio.run(main())
