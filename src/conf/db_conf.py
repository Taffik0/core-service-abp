from src.logger import logger
from .env import get_env

DATABASE = get_env("DATABASE")
DB_URL = get_env("DB_URL")
USER = get_env("USER")
PASSWORD = get_env("PASSWORD")
logger.info(f"url {DATABASE=}")
logger.info(f"url {DB_URL=}")
logger.info(f"url {USER=}")