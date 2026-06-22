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
    env_exists = CONDA_ENV in result.stdout

    if env_exists:
        print(f"   Env already exists — checking installed version.")
        ver_result = subprocess.run(
            ["conda", "run", "-n", CONDA_ENV, "pip", "show", "litellm"],
            capture_output=True, text=True
        )
        installed_version = None
        for line in ver_result.stdout.splitlines():
            if line.startswith("Version:"):
                installed_version = line.split(":", 1)[1].strip()
        if installed_version:
            print(f"   Found litellm=={installed_version}")
            if installed_version != LITELLM_VERSION:
                print(f"   WARNING: expected {LITELLM_VERSION}, found {installed_version} — continuing.")
        else:
            print(f"   WARNING: could not determine installed litellm version — continuing.")
    else:
        subprocess.run(
            ["conda", "create", "-y", "-n", CONDA_ENV, f"python={PYTHON_VERSION}"],
            check=True
        )
        print(f"── Installing litellm[proxy]=={LITELLM_VERSION}")
        subprocess.run(
            ["conda", "run", "-n", CONDA_ENV, "pip", "install", f"litellm[proxy]=={LITELLM_VERSION}"],
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
