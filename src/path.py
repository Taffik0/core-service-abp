from pathlib import Path

file_path = Path(__file__).resolve()  # полный путь к файлу
src_path = file_path.parent
root_path = src_path.parent

ROOT_PATH = root_path
LOGS_DIR = root_path / "logs"
