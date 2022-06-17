from pathlib import Path
import re

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from constants import DEFAULT_FILTERS


@dataclass(frozen=True)
class Filter(DataClassJsonMixin):
    name: str
    filter_expression: str
    category: str
    order: int

    def match(self, value):
        return bool(re.search(self.filter_expression, value))

    def __lt__(self, val: "Filter") -> bool:
        return self.order < val.order

    def __gt__(self, val: "Filter") -> bool:
        return self.order > val.order

    def __ge__(self, val: "Filter") -> bool:
        return self.order >= val.order

    def __le__(self, val: "Filter") -> bool:
        return self.order <= val.order

    def __ne__(self, val: "Filter") -> bool:
        return self.order != val.order


@dataclass
class FilterList(DataClassJsonMixin):
    filters: list[Filter] = []

    @classmethod
    def load(cls, file_path: Path = DEFAULT_FILTERS) -> "FilterList":
        if not file_path.exists():
            return cls()
        with open(file_path, "r+") as f:
            cls.from_json(f.read())

    def save(self, file_path: Path = DEFAULT_FILTERS) -> None:
        with open(file_path, "w+") as f:
            f.write(self.to_json())
