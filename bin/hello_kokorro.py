from kokoro_client import KokoroClient

client = KokoroClient()
result = client.synthesize("Hello world", job_id="001", output_dir="/tmp")
files = client.download_all("001", result["files"], dest="/tmp/downloaded")
