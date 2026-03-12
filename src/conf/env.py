from src.path import ROOT_PATH

from dotenv import load_dotenv
import os

load_dotenv(ROOT_PATH / ".env", override=True)
load_dotenv(ROOT_PATH / ".env.urls", override=True)
load_dotenv(ROOT_PATH / ".env.db", override=True)


def get_env(name: str, default=None):
    value = os.environ.get(name, default)
    if value is None:
        raise RuntimeError(f"Env variable {name} is required")
    return value
