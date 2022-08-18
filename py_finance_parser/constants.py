from os import environ
from pathlib import Path

CWD: Path = Path.cwd()

DEFAULT_DATA_DIRECTORY: Path = CWD / "data"
DEFAULT_RAW_DIRECTORY: Path = DEFAULT_DATA_DIRECTORY / "raw"
DEFAULT_CLEANSED_DIRECTORY: Path = DEFAULT_DATA_DIRECTORY / "cleansed"
DEFAULT_PARSED_DIRECTORY: Path = DEFAULT_DATA_DIRECTORY / "parsed"
try:
    USER_DIRECTORY: Path = Path(environ["HOME"])
except KeyError:
    USER_DIRECTORY: Path = Path(environ["USERPROFILE"])

DOCUMENTS_DIRECTORY: Path = USER_DIRECTORY / "Documents"

CSV_FILE_PATTERN: str = "*.csv"
JSON_FILE_PATTERN: str = "*.json"
