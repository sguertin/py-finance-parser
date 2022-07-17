import csv
from pathlib import Path

from py_finance_parser.models.transaction import Transaction
from py_finance_parser.services.file import DataFileService


class TransactionFileService:
    data_file_service: DataFileService

    def __init__(self, data_file_service: DataFileService = None):
        if data_file_service is None:
            data_file_service = DataFileService()
        self.data_file_service = data_file_service

    def load_latest_raw(self):
        file_path = self.data_file_service.raw_directory()
        return self.parse_csv_file(file_path)

    def parse_json_file(self, file_path: Path) -> list[Transaction]:
        with open(file_path, "r+") as f:
            return Transaction.json_to_list(f.read())

    def parse_csv_file(
        self, file_path: Path, starting_id: int = 1
    ) -> list[Transaction]:
        with open(file_path, "r+") as f:
            return [
                Transaction.create_from_csv_row(n + starting_id, row)
                for n, row in enumerate(csv.reader(f))
            ]

    def save_parsed_transaction_file(
        self, file_path: Path, transactions: list[Transaction]
    ) -> None:
        with open(file_path, "w+") as f:
            f.write(Transaction.list_to_json(transactions))
