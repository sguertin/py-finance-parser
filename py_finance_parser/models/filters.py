from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal as decimal

from pandas import DataFrame, Series

from models.enums import Category, Comparison, Column


class Condition(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_query") and callable(subclass.get_query)
        ) or NotImplemented
    
    def __str__(self) -> str:
        return self.get_query()

    @abstractmethod
    def get_query(self) -> str:
        raise NotImplementedError(self.get_query)

@dataclass(slots=True)
class StringMatchCondition(Condition):
    match_phrase: str

    def get_query(self):
        return f"{Column.DESCRIPTION}.str.contains('{self.match_phrase}')"

@dataclass(slots=True)
class ValueCondition(Condition):
    value: decimal
    comparison: Comparison = Comparison.EQUAL_TO

    def get_query(self) -> str:
        return f"{Column.AMOUNT} {self.comparison} {self.value:2f}"

@dataclass(slots=True)
class ValueRangeCondition(Condition):
    from_value: float
    to_value: float

    def get_query(self) -> str:
        return f"{self.from_value:2f} <= {Column.AMOUNT} <= {self.to_value:2f}"

@dataclass(slots=True)
class DateRangeCondition(Condition):
    from_date: datetime
    to_date: datetime

    def __init__(self, from_date: datetime, to_date: datetime = None):
        if to_date is None:
            to_date = from_date
        self.to_date = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 00)
        self.from_date = datetime(
            from_date.year, from_date.month, from_date.day, 0, 0, 0
        )

    def get_query(self) -> Series:
        return f"{self.from_date:%Y%m%d} <= {Column.DATE} <= {self.to_date:%Y%m%d}"

@dataclass(slots=True)
class CategoryCondition(Condition):
    category: Category
    
    def get_query(self) -> str:
        return f"{Column.CATEGORY} == {self.category}"

UNCATEGORIZED_CONDITION = CategoryCondition(Category.UNCATEGORIZED)

LOGICAL_AND = " AND "
LOGICAL_OR = " OR "

@dataclass(slots=True)
class Filter:
    name: str
    category: Category
    conditions: list[Condition] 
    tags: list[str] = field(default_factory=list)
    override: bool = False

    def get_matches(self, df: DataFrame) -> Series:
        conditions = self.conditions
        if not self.override:
            conditions.append(UNCATEGORIZED_CONDITION)
        return df.eval(LOGICAL_AND.join(f"{condition}" for condition in conditions))

        
