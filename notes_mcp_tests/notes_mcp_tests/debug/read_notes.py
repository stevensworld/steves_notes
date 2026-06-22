import asyncio
import json
from fastmcp import Client
from notes_mcp.server import mcp


async def main():
    async with Client(mcp) as client:
        await client.call_tool("new_iterator")
        count = 0
        while True:
            result = await client.call_tool("get_next_note")
            text = result.content[0].text if result.content else ""
            if "All" in text and "visited" in text:
                print(text)
                break
            note = json.loads(text)
            count += 1
            print(f"── Note {count}: {note.get('name', '')} [{note.get('node_id', '')}]")
            print(f"   topic: {note.get('topic', '')}")
            print(f"   text:  {note.get('text', '')}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
