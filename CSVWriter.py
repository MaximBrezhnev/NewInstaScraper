import csv


class CSVWriter:
    def __init__(self, filename: str, headers: list[str]):
        self.filename = filename
        self.headers = headers

        with open(self.filename, 'wt', encoding='utf-8') as file:
            file.write('')

        with open(self.filename, 'at', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

    def add_new_account(self, account):
        with open(self.filename, 'at', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([x if x else "нету" for x in account.model_dump().values()])

    def add_information_about_fail(self):
        with open(self.filename, "at", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["-" for i in range(6)])
