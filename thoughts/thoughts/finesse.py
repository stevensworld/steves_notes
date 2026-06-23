import json
import urllib.request

CONFIG = {
    "host": "localhost",
    "port": 4000,
    "model": "gemma",
}

SYSTEM_PROMPT = """You are a strict text-processing utility designed to prepare apprentice study notes for a Text-to-Speech (TTS) engine.

CRITICAL INSTRUCTION - ACRONYM LETTER SPOKEN ISOLATION:
Whenever an acronym, abbreviation, or trade shorthand appears, you must expand it so that EACH individual letter is pronounced distinctly by the speech engine as a standalone letter-name.

Apply these exact phonetic expansions:
- 'AIT' must be written as 'Ay Eye Tee'
- 'ILM' must be written as 'I L M'
- 'NC' must be written as 'normally closed'
- 'NO' must be written as 'normally open'
- 'IC' must be written as 'instantaneous contacts'
- 'TDOD' must be written as 'time delay on de-energization'
- 'TDOE' must be written as 'time delay on energization'
- 'NEMA' must be written as 'Neema'
- 'T1, T4' must be written as 'lead markings T-one and T-four'
- 'µF' or 'uF' must be written as 'microfarads'
- 'µH' or 'uH' must be written as 'microhenries'

AUDIO FORMATTING CONSTRAINTS:
1. Write strictly for the ear. Spell out all numbers, units, and symbols completely.
2. Maintain the raw note's structural flow, but ensure natural pausing punctuation (commas, periods) is used so the TTS engine delivers a clean delivery."""


def finesse(raw_text: str, objective: str, topic: str, config: dict = None) -> str:
    cfg = {**CONFIG, **(config or {})}
    url = f"http://{cfg['host']}:{cfg['port']}/chat/completions"

    user_payload = (
        f"--- APPRENTICESHIP STUDY CONTEXT ---\n"
        f"CURRENT UNIT OBJECTIVE: {objective}\n"
        f"TOPIC SCOPE: {topic}\n"
        f"-------------------------------------\n\n"
        f"RAW NOTE DATA OR QUESTION FRAGMENT TO DEVELOP:\n"
        f"\"{raw_text}\"\n\n"
        f"Please transform this raw fragment into a polished active-recall audio transcript matching the system instructions."
    )

    payload = json.dumps({
        "model": cfg["model"],
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_payload},
        ],
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        response = json.loads(r.read().decode())

    return response["choices"][0]["message"]["content"].strip()
