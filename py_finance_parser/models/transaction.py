from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum
from dataclasses_json import DataClassJsonMixin

from py_finance_parser.mixins.dataclasses_json import ListDataClassJsonMixin


class Columns(IntEnum):
    DATE = 0
    DESCRIPTION = 1
    AMOUNT = 2
    RUNNING_BALANCE = 3


class Category(Enum):
    UNCATEGORIZED = "Uncategorized"
    MORTGAGE = "Mortgage"
    TAXES = "Taxes"
    ELECTRIC = "Electric"
    GAS = "Gas"
    INTERNET = "Internet"
    PHONE = "Phone"
    LOANS = "Loans"
    ENTERTAINMENT = "Entertainment"
    AUTO = "Auto"
    GROCERIES = "Groceries"
    PETS = "Pets"
    DATE_NIGHTS = "Date Nights"
    FITNESS = "Gym Fees"


@dataclass
class Transaction(ListDataClassJsonMixin):
    id: int
    date: datetime
    description: str
    amount: float
    running_balance: float
    category: Category

    @classmethod
    def create_from_csv_row(cls, id, row: list[str]) -> "Transaction":
        month, day, year = row[Columns.DATE].split("/")
        return cls(
            id,
            datetime(int(year), int(month), int(day)),
            row[Columns.DESCRIPTION],
            float(row[Columns.AMOUNT]),
            float(row[Columns.RUNNING_BALANCE]),
            Category.UNCATEGORIZED,
        )

    def __ne__(self, trx: "Transaction") -> bool:
        return self.id != trx.id

    def __eq__(self, trx: "Transaction") -> bool:
        return self.id == trx.id

    def __gt__(self, trx: "Transaction") -> bool:
        return self.id > trx.id

    def __ge__(self, trx: "Transaction") -> bool:
        return self.id >= trx.id

    def __lt__(self, trx: "Transaction") -> bool:
        return self.id < trx.id

    def __le__(self, trx: "Transaction") -> bool:
        return self.id <= trx.id


@dataclass
class TransactionList(DataClassJsonMixin):
    transactions: list[Transaction]
    created: datetime

    def __init__(self, transactions: list[Transaction]):
        self.transactions = transactions
        self.created = datetime.now()
