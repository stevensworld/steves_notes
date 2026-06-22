import os
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, COMM, USLT, error


class AudioTagger:
    def __init__(self, notes_file: str = "notes.json", mp3_dir: str = None):
        self.notes_file = notes_file
        self.mp3_dir = mp3_dir or os.getcwd()

    def run(self):
        if not os.path.exists(self.notes_file):
            print(f"Error: '{self.notes_file}' not found.")
            return

        with open(self.notes_file, "r", encoding="utf-8") as f:
            module_data = json.load(f)

        module_name = module_data.get("name", "Unknown Module")
        print(f"Tagging MP3s for module: {module_name}")

        for obj_node in module_data.get("children", []):
            if obj_node.get("type") == "objective":
                obj_name = obj_node.get("name", "Unknown Objective")
                for note in obj_node.get("children", []):
                    if note.get("type") == "note":
                        note_id = note.get("id")
                        note_name = note.get("name")
                        text_content = note.get("metadata", {}).get("text_content", note_name)
                        file_path = os.path.join(self.mp3_dir, f"{note_id}.mp3")
                        self._tag(file_path, note_name, text_content, module_name, obj_name)

        print("Done.")

    def tag_note(self, node_id: str):
        if not os.path.exists(self.notes_file):
            return
        with open(self.notes_file, "r", encoding="utf-8") as f:
            module_data = json.load(f)
        module_name = module_data.get("name", "Unknown Module")
        for obj_node in module_data.get("children", []):
            if obj_node.get("type") == "objective":
                obj_name = obj_node.get("name", "Unknown Objective")
                for note in obj_node.get("children", []):
                    if note.get("type") == "note" and note.get("id") == node_id:
                        file_path = os.path.join(self.mp3_dir, f"{node_id}.mp3")
                        self._tag(file_path, note.get("name"), note.get("metadata", {}).get("text_content", ""), module_name, obj_name)
                        return

    def _tag(self, file_path: str, title: str, text: str, module_name: str, obj_name: str):
        if not os.path.exists(file_path):
            return
        try:
            audio = MP3(file_path, ID3=ID3)
            try:
                audio.add_tags()
            except error:
                pass
            audio.tags.add(TIT2(encoding=3, text=title))
            audio.tags.add(COMM(encoding=3, lang='eng', desc='Lineage', text=f"{module_name} -> {obj_name}"))
            audio.tags.add(USLT(encoding=3, lang='eng', desc='', text=text))
            audio.save()
            print(f"  tagged: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  error tagging {os.path.basename(file_path)}: {e}")


if __name__ == "__main__":
    AudioTagger().run()
