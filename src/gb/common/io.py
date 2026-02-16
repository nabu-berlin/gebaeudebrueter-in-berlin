from pathlib import Path


def ensure_parent_dir(file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
