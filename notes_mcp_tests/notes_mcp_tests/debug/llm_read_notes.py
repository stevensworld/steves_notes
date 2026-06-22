import asyncio
import json
import urllib.request
from fastmcp import Client
from notes_mcp.server import mcp

LITELLM_URL = "http://localhost:4000/chat/completions"
MODEL = "gemma"


def summarize(note_text: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"Summarize this note in one sentence:\n\n{note_text}"}
        ]
    }).encode()
    req = urllib.request.Request(
        LITELLM_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        response = json.loads(r.read().decode())
    return response["choices"][0]["message"]["content"].strip()


async def main():
    async with Client(mcp) as client:
        await client.call_tool("new_iterator")
        count = 0
        while True:
            result = await client.call_tool("get_next_note")
            text = result.content[0].text if result.content else ""
            if "All" in text and "visited" in text:
                print(f"\n── Done. {count} notes summarized.")
                break
            note = json.loads(text)
            count += 1
            note_text = note.get("text", "") or note.get("metadata", {}).get("text_content", "")
            print(f"\n── Note {count}: {note.get('name', '')} [{note.get('node_id', '')}]")
            print(f"   topic: {note.get('topic', '')}")
            summary = summarize(note_text)
            print(f"   summary: {summary}")


if __name__ == "__main__":
    asyncio.run(main())
