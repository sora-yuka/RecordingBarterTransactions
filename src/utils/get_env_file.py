from pathlib import Path

def find_env_file() -> Path:
    current = Path(__file__).resolve()

    for parent in [current] + list(current.parents):
        env_path = parent / ".env"

        if env_path.is_file():
            return env_path
    return Path.cwd() / ".env"
