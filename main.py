import os

from CSVWriter import CSVWriter
from config import config
from get_parser import get_parser
from schemas import Account
from utils import read_accounts_from_csv


def main():
    parser = get_parser(
        username=config.ig_username,
        password=config.ig_password,
        session_file=config.session_file,
    )

    link = input("Вставьте ссылку на профиль: ")
    pars = input(
        "Кого будем парсить? Если тех, кто подписан на профиль - введите 1, если тех, на кого подписан профиль - "
        "введите 2."
    )
    username = get_username_from_url(profile_url=link)
    if pars == '1':
        accounts_to_parse = parser.get_followers(username=username)
    else:
        accounts_to_parse = parser.get_following(username=username)

    writer = CSVWriter(
        filename='parsing.csv',
        headers=list(Account.model_fields.keys()),
    )

    eta = len(accounts_to_parse)
    print(f"{eta} аккаунтов будем парсить")
    accounts_for_login = read_accounts_from_csv("accounts.csv")
    account_number = -1
    max_i = eta

    for i, account in enumerate(accounts_to_parse, start=1):
        if i % 900 == 0:
            while account_number + 1 < len(accounts_for_login):
                account_number += 1
                try:
                    os.remove(config.session_file)
                    parser = get_parser(
                        username=accounts_for_login[account_number][0],
                        password=accounts_for_login[account_number][1],
                        session_file=config.session_file
                    )
                    print(f"Теперь парсинг производится с аккаунта {parser.username}!")
                    break
                except Exception:
                    print(f"Парсинг с аккаунта {accounts_for_login[account_number][0]} не возможен на данный момент!")
                    max_i = eta - 900

        if i >= max_i:
            break

        try:
            print(f"получаем {account}")
            info = parser.get_user_info(account)
            writer.add_new_account(info)
            print(f"получили {info.login}, это {i}/{eta}.")
        except:
            continue

    print(f"Результат сохранен в файл по адресу ~/{writer.filename}")


def get_username_from_url(profile_url: str) -> str:
    parts = profile_url.split('/')
    if len(parts) > 3 and "instagram.com" in parts[2]:
        return parts[3]
    else:
        raise ValueError("Неверный URL профиля Instagram")


main()
