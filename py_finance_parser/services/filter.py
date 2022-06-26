from pathlib import Path

from py_finance_parser.constants import DEFAULT_FILTERS_FILES
from py_finance_parser.models.filter import Filter
from py_finance_parser.models.transaction import Transaction, TransactionList, Category


class FilteringService:
    file_path: Path

    def __init__(self, file_path: Path = None):
        if file_path is None:
            file_path = DEFAULT_FILTERS_FILES
        self.file_path = file_path

    def filter_transactions(self, transaction_list: TransactionList) -> None:
        filter_list = self.get_filter_list()
        return [
            self.filter_transaction(trx, filter_list)
            for trx in transaction_list.transactions
            if trx.category == Category.UNCATEGORIZED
        ]

    def filter_transaction(self, trx: Transaction, filter_list: list[Filter]):
        for filter in filter_list:
            if self.apply_filter(trx, filter):
                break

    def apply_filter(self, trx: Transaction, filter: Filter):
        if filter.match(trx.description):
            trx.category = filter.category
            return True
        return False

    def get_filter_list(self) -> list[Filter]:
        if not self.file_path.exists():
            return []
        with open(self.file_path, "r+") as f:
            Filter.json_to_list(f.read())

    def save_filter_list(self, filter_list: list[Filter]) -> None:
        with open(self.file_path, "w+") as f:
            f.write(Filter.list_to_json(filter_list))
