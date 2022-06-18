import csv
from pathlib import Path

from py_finance_parser.models.transaction import Transaction, TransactionList


class TransactionFileParsingService:
    file_path: Path

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def parse_transaction_file(self, starting_id: int = 1) -> TransactionList:
        with open(self.file_path, "r+") as f:
            contents = [_ for _ in csv.reader(f)]
            result = [
                Transaction.create_from_csv_row(n + starting_id, row)
                for n, row in enumerate(contents)
            ]
        return TransactionList(result)

    def save_parsed_transaction_file(self, transactions: TransactionList) -> None:
        with open(self.file_path, "w+") as f:
            f.write(transactions.to_json())
