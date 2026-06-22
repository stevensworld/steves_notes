import subprocess
import sys

CONDA_ENV = "litellm_secure_env"
PYTHON_VERSION = "3.11"
LITELLM_VERSION = "1.82.6"


def setup():
    print(f"── Creating conda env: {CONDA_ENV} (Python {PYTHON_VERSION})")

    result = subprocess.run(
        ["conda", "env", "list"],
        capture_output=True, text=True
    )
    if CONDA_ENV in result.stdout:
        print(f"   Env already exists — skipping create.")
    else:
        subprocess.run(
            ["conda", "create", "-y", "-n", CONDA_ENV, f"python={PYTHON_VERSION}"],
            check=True
        )

    print(f"── Installing litellm=={LITELLM_VERSION}")
    subprocess.run(
        ["conda", "run", "-n", CONDA_ENV, "pip", "install", f"litellm=={LITELLM_VERSION}"],
        check=True
    )

    print(f"── Verifying installation")
    result = subprocess.run(
        ["conda", "run", "-n", CONDA_ENV, "litellm", "--version"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"   litellm version: {result.stdout.strip()}")
        print(f"── Done.")
    else:
        print(f"   ERROR: litellm not found after install.")
        sys.exit(1)


if __name__ == "__main__":
    setup()
