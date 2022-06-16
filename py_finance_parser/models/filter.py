import re

from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


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
    filters: list[Filter]
