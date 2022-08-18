from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal as decimal
import re

from pandas import DataFrame, Series

from models.enums import Category, Comparison, Column


class Condition(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "match") and callable(subclass.match) and
            hasattr(subclass, "get_query") and callable(subclass.get_query)
        ) or NotImplemented

    def get_query(self):
        raise NotImplementedError(self.get_query)
    
    @abstractmethod
    def match(self, df: DataFrame) -> Series:
        raise NotImplementedError(self.match)


@dataclass
class Filter:
    name: str
    category: Category
    conditions: list[Condition]
    tags: list[str] = field(default_factory=list)

    def match(self, df: DataFrame) -> Series:
        mask = Series([True for _ in range(df.size)])
        for condition in self.conditions:
            mask = mask & condition.match(df)
        return mask


@dataclass(slots=True)
class StringMatchCondition(Condition):
    match_phrase: str
    
    def get_query(self):
        return f"{Column.DESCRIPTION}.str.contains('{self.match_phrase}')"
    
    def match(self, df: DataFrame) -> Series:
        df[str(Column.DESCRIPTION)].str.contains(self.match_phrase, flags=re.IGNORECASE)


@dataclass(slots=True)
class ValueCondition(Condition):
    value: decimal
    comparison: Comparison = Comparison.EQUAL_TO

    def match(self, df: DataFrame) -> Series:
        return df.query(f"{df[str(Column.AMOUNT)]} {self.comparison} {self.value:2f}")


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

    def match(self, df: DataFrame) -> Series:
        return df.query(
            f"{self.from_date:%Y%m%d} <= {Column.DATE} <= {self.to_date:%Y%m%d}"
        )


# @dataclass(slots=True)
# class DescriptionFilter(Filter):
#     name: str
#     category: Category
#     filter_expression: str
#     subfilter: Filter
#     tags: list[str]

#     def __init__(
#         self,
#         name: str,
#         filter_expression: str,
#         category: Category = None,
#         subfilter: Filter = None,
#         tags: list[str] = None,
#     ):
#         """Initializes a filter that will try to find a match for the regular expression provided and returns a match if true

#         Args:
#             name (str): the name for the filter
#             filter_expression (str): the regular expression to compare against the transaction description
#             category (Category): the category associated with this filter
#         """
#         if tags is None:
#             tags = []
#         self.name = name
#         self.filter_expression = filter_expression
#         self.category = category
#         self.tags = tags
#         self.subfilter = subfilter

#     def match(self, df: DataFrame) -> Series:
#         try:
#             if self.subfilter:
#                 subfilter_mask = self.subfilter.match(df.copy())
#             else:
#                 subfilter_mask = Series([True for _ in range(df.size)])
#             return (
#                 df.description.str.contains(self.filter_expression, flags=re.IGNORECASE)
#                 & subfilter_mask
#             )
#         except Exception as ex:
#             handle_ex(self, ex)


# @dataclass(slots=True)
# class ValueFilter(Filter):
#     name: str
#     category: Category
#     limit: float
#     comparison: Comparison
#     subfilter: Filter
#     tags: list[str]

#     def __init__(
#         self,
#         name: str,
#         limit: float,
#         category: Category,
#         comparison: Comparison = Comparison.EQUAL_TO,
#         subfilter: str | Filter = None,
#         tags: list[str] = None,
#     ):
#         """Initialize a ValueFilter, all value filters are applied as follows 'transaction.amount is <comparison> filter.limit',
#             e.g. transaction.amount is GREATER_THAN_OR_EQUAL_TO filter.limit

#             If a filter expression is also included that will be matched as well, and BOTH must match for the comparison to return True
#             NOTE: Comparisons are done against absolute values i.e. +/- signs will be ignored
#         Args:
#             name (str): The name for this filter
#             limit (str): The decimal value you wish to compare to
#             comparison (Comparison): The comparison operation
#             category (Category): the category to apply when matching this filter
#             subfilter (str|DescriptionFilter, optional): A text phrase to be matched in the transaction's description. Defaults to None.
#             order (int, optional): The order the filters should be applied. Defaults to 0.
#         """
#         if type(subfilter) is str:
#             subfilter = DescriptionFilter(f"{name}-subfilter", subfilter, category)
#         if tags is None:
#             tags = []
#         self.name = name
#         self.limit = limit
#         self.comparison = comparison
#         self.category = category
#         self.subfilter = subfilter
#         self.tags = tags

#     def match(self, df: DataFrame) -> Series:
#         try:
#             if self.subfilter:
#                 subfilter_mask = self.subfilter.match(df.copy())
#             else:
#                 subfilter_mask = Series([True for _ in range(df.size)])
#             limit = decimal(f"{self.limit:2f}")
#             if self.comparison == Comparison.EQUAL_TO:
#                 return df.amount == limit & subfilter_mask
#             elif self.comparison == Comparison.NOT_EQUAL_TO:
#                 return df.amount != limit & subfilter_mask
#             elif self.comparison == Comparison.GREATER_THAN:
#                 return df.amount > limit & subfilter_mask
#             elif self.comparison == Comparison.GREATER_THAN_EQUAL_TO:
#                 return df.amount >= limit & subfilter_mask
#             elif self.comparison == Comparison.LESS_THAN:
#                 return df.amount < limit & subfilter_mask
#             elif self.comparison == Comparison.LESS_THAN_EQUAL_TO:
#                 return df.amount <= limit & subfilter_mask
#             raise ValueError(self.comparison)
#         except Exception as ex:
#             handle_ex(self, ex)


# @dataclass(slots=True)
# class AmazonFilter(ValueFilter):
#     name: str
#     category: Category
#     limit: decimal
#     comparison: Comparison
#     subfilter: Filter
#     tags: list[str]

#     def __init__(
#         self,
#         limit: decimal,
#         category: Category = None,
#         comparison: Comparison = Comparison.EQUAL_TO,
#         tags: list[str] = None,
#     ):
#         self.name = f"AmazonFilter(amount {comparison} ${limit})"
#         self.limit = decimal(limit)
#         self.comparison = comparison
#         self.category = category
#         if tags is None:
#             tags = []
#         self.tags = tags
#         self.subfilter = AMAZON_SUBFILTER


# @dataclass(slots=True)
# class DateRangeFilter:
#     name: str
#     from_date: datetime
#     to_date: datetime
#     subfilter: Filter
#     tags: list[str] = field(default_factory=list)

#     def __init__(
#         self,
#         from_date: datetime,
#         to_date: datetime,
#         category: Category = None,
#         subfilter: Filter | str = None,
#         tags: list[str] = field(default_factory=list),
#     ):
#         self.name = f"DateRangeFilter({from_date:%Y-%m-%d} < date < {to_date:%Y-%m-%d})"
#         if type(subfilter) is str:
#             subfilter = DescriptionFilter(f"{self.name}-subfilter", subfilter, category)
#         if subfilter is not None:
#             self.name = self.name + f" - {subfilter.name}"
#             tags = list(set(tags.extend(subfilter.tags)))
#         self.from_date = from_date
#         self.to_date = to_date
#         self.subfilter = subfilter
#         self.tags = tags

#     @property
#     def category(self) -> Category:
#         return self.subfilter.category

#     def match(self, df: DataFrame) -> Series:
#         try:
#             if self.subfilter:
#                 subfilter_mask = self.subfilter.match(df.copy())
#             else:
#                 subfilter_mask = Series([True for _ in range(df.size)])
#             return (
#                 df.query(f"{self.from_date:%Y%m%d} < date < {self.to_date:%Y%m%d}")
#                 & subfilter_mask
#             )
#         except Exception as ex:
#             handle_ex(self, ex)
