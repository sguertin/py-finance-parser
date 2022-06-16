import csv
from models.transaction import Transaction, TransactionList


class TransactionParsingService:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse_transaction_file(self, starting_id: int = 1) -> TransactionList:
        result = []
        with open(self.file_path, "r+") as f:
            contents = csv.reader(f)
            n = starting_id
            for row in contents:
                result.append(Transaction.create_from_csv_row(n, row))
                n += 1
        return TransactionList(result)

    def save_parsed_transaction_file(self, transactions: TransactionList):
        with open(self.file_path, "w+") as f:
            f.write(transactions.to_json())
