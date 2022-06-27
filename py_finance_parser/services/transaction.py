import csv
from pathlib import Path

from py_finance_parser.models.transaction import Transaction, TransactionList


class TransactionFileParsingService:
    file_path: Path

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def parse_csv_file(self, starting_id: int = 1) -> list[Transaction]:
        with open(self.file_path, "r+") as f:
            contents = [_ for _ in csv.reader(f)]
            return [
                Transaction.create_from_csv_row(n + starting_id, row)
                for n, row in enumerate(contents)
            ]

    def save_parsed_transaction_file(self, transactions: list[Transaction]) -> None:
        with open(self.file_path, "w+") as f:
            f.write(Transaction.list_to_json(transactions))
