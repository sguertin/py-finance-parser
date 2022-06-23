from dataclasses import dataclass
from pathlib import Path
import re

from py_finance_parser.constants import DEFAULT_FILTERS
from py_finance_parser.mixins.dataclasses_json import ListDataClassJsonMixin


@dataclass(frozen=True)
class Filter(ListDataClassJsonMixin):
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
