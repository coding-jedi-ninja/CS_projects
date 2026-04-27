import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = BASE_DIR / "data"
SEED_DATA_DIR = BASE_DIR / "deploy_seed_data"
DATA_DIR = Path(os.getenv("CAMPUS_CAFE_DATA_DIR", DEFAULT_DATA_DIR)).resolve()


def data_file(filename: str) -> Path:
    """
    Return the full path for a data file, seed it if needed, and ensure the
    directory exists.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    target = DATA_DIR / filename
    seed = SEED_DATA_DIR / filename

    if not target.exists() and seed.exists():
        target.write_bytes(seed.read_bytes())

    return target
