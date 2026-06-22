import json
import os
import urllib.request

CONFIG = {
    "host": "localhost",
    "port": 4001,
}


class KokoroClient:
    def __init__(self, config: dict = None):
        self._config = {**CONFIG, **(config or {})}
        self._base = f"http://{self._config['host']}:{self._config['port']}"

    def health(self) -> dict:
        with urllib.request.urlopen(f"{self._base}/health", timeout=3) as r:
            return json.loads(r.read().decode())

    def synthesize(self, text: str, job_id: str, output_dir: str, voice: str = "af_heart", speed: float = 1.0) -> dict:
        payload = json.dumps({
            "text": text,
            "job_id": job_id,
            "output_dir": output_dir,
            "voice": voice,
            "speed": speed,
        }).encode()
        req = urllib.request.Request(
            f"{self._base}/synthesize",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode())

    def download(self, job_id: str, filename: str, dest: str) -> str:
        url = f"{self._base}/download/{job_id}/{filename}"
        os.makedirs(dest, exist_ok=True)
        filepath = os.path.join(dest, filename)
        urllib.request.urlretrieve(url, filepath)
        return filepath

    def download_all(self, job_id: str, files: list, dest: str) -> list:
        return [self.download(job_id, f, dest) for f in files]
