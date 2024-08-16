import csv
import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def read_accounts_from_csv(file_path):
    accounts = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            accounts.append((row[0], row[1]))
    return accounts
