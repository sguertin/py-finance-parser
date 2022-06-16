from pathlib import Path

from py_finance_parser.models.filter import FilterList, Filter
from py_finance_parser.models.transaction import Transaction, TransactionList, Category


class FilteringService:
    file_path: str

    def __init__(self, file_path):
        self.file_path = file_path

    def filter_transactions(self, transaction_list: TransactionList) -> None:
        filter_list = self.get_filter_list()
        return [
            self.filter_transaction(trx, filter_list)
            for trx in transaction_list.transactions
            if trx.category == Category.UNCATEGORIZED
        ]

    def filter_transaction(self, trx: Transaction, filter_list: FilterList):
        for filter in filter_list.filters:
            if self.apply_filter(trx, filter):
                break

    def apply_filter(self, trx: Transaction, filter: Filter):
        if filter.match(trx.description):
            trx.category = filter.category
            return True
        return False

    def get_filter_list(self) -> FilterList:
        if not Path(self.file_path).exists():
            return FilterList()
        with open(self.file_path, "r+") as f:
            FilterList.from_json(f.read())

    def save_filter_list(self, filter_list: FilterList) -> None:
        with open(self.file_path, "w+") as f:
            f.write(filter_list.to_json())
