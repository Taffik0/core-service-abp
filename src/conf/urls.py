from src.logger import logger
from .env import get_env

BROKER_URL = get_env("BROKER_URL")
logger.info(f"url {BROKER_URL=}")