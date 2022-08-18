from enum import Enum, IntEnum


class StringEnum(Enum):
    def __str__(self) -> str:
        return self.value


class Category(StringEnum):
    """An Enumeration of categories for transactions to be placed in"""

    AMAZON = "Amazon"
    AUTO = "Auto"
    DATE_NIGHTS = "Date Nights"
    DELIVERY = "Delivery"
    ELECTRIC = "Electric"
    ENTERTAINMENT = "Entertainment"
    FITNESS = "Gym Fees"
    FRAUD = "Fraud"
    GAS = "Gas"
    GIFTS = "Gifts"
    GROCERIES = "Groceries"
    GRUBHUB = "Grubhub"
    INCOME = "Income"
    INSURANCE = "Insurance"
    INTERNET = "Internet"
    LOANS = "Loans"
    MORTGAGE = "Mortgage"
    PETS = "Pets"
    PHONE = "Phone"
    SAVINGS = "Savings"
    TAKEOUT = "Takeout"
    TAXES = "Taxes"
    WEED = "Weed"
    UNCATEGORIZED = "Uncategorized"

    def __str__(self) -> str:
        return self.value


class Column(StringEnum):
    DATE = "date"
    DESCRIPTION = "description"
    AMOUNT = "amount"
    RUNNING_BALANCE = "running balance"
    CATEGORY = "category"
    TAGS = "tags"
    ID = "id"


class Comparison(StringEnum):
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL_TO = ">="
    EQUAL_TO = "=="
    NOT_EQUAL_TO = "!="
    LESS_THAN = "<"
    LESS_THAN_EQUAL_TO = "<="

    def __str__(self) -> str:
        return self.value


class Month(IntEnum):
    """The Month of the Year starting at 1 for January, up to 12 for December"""

    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12
