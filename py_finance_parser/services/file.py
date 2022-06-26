from pathlib import Path

from py_finance_parser.constants import (
    DEFAULT_CLEANSED_DIRECTORY,
    DEFAULT_RAW_DIRECTORY,
    DEFAULT_PARSED_DIRECTORY,
    CSV_FILE_PATTERN,
    JSON_FILE_PATTERN,
)


class DataFileService:
    raw_directory: Path
    cleansed_directory: Path
    parsed_directory: Path

    def __init__(
        self,
        raw_directory: Path = None,
        cleansed_directory: Path = None,
        parsed_directory: Path = None,
    ):
        if raw_directory is None:
            raw_directory = DEFAULT_RAW_DIRECTORY
        if cleansed_directory is None:
            cleansed_directory = DEFAULT_CLEANSED_DIRECTORY
        if parsed_directory is None:
            parsed_directory = DEFAULT_PARSED_DIRECTORY
        self.raw_directory = raw_directory
        self.cleansed_directory = cleansed_directory
        self.parsed_directory = parsed_directory

    def get_latest_raw(self) -> Path:
        return self.get_latest(self.raw_directory, CSV_FILE_PATTERN)

    def get_all_raw(self) -> Path:
        return self.get_files(self.raw_directory, CSV_FILE_PATTERN)

    def get_latest_cleansed(self) -> Path:
        return self.get_latest(self.cleansed_directory, CSV_FILE_PATTERN)

    def get_all_cleansed(self) -> list[Path]:
        return self.get_files(self.cleansed_directory, CSV_FILE_PATTERN)

    def get_latest_parsed(self) -> Path:
        return self.get_latest(self.parsed_directory, JSON_FILE_PATTERN)

    def get_all_parsed(self) -> list[Path]:
        return self.get_files(self.parsed_directory, JSON_FILE_PATTERN)

    def get_latest(self, directory: Path, filename_pattern: str) -> Path:
        files = self.get_files(directory, filename_pattern)
        return max(files, key=lambda x: x.stat().st_ctime)

    def get_files(self, directory: Path, filename_pattern: str = "*") -> list[Path]:
        if not directory.is_dir():
            raise ValueError(f"Path provided '{directory}' is not a directory")
        return [file for file in directory.glob(filename_pattern) if not file.is_dir()]
