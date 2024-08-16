from datetime import datetime

from instauto.api.client import ApiClient
from instauto.api.actions.structs.profile import Info
from instauto.api.exceptions import CorruptedSaveData
from instauto.helpers.friendships import get_followers, get_following, get_user_id_from_username
from instauto.helpers.post import retrieve_posts_from_user

from schemas import Account
from utils import read_accounts_from_csv


class AutoParser:
    def __init__(
            self,
            username: str = None,
            password: str = None,
            session_file: str = None,
    ):
        self.username = username
        self.password = password
        self.session_file = session_file

        if session_file:
            print(f"Инициализация из файла {session_file}")
            try:
                self.client = ApiClient.initiate_from_file(session_file)
                print("Инициализация успешна")
                return
            except FileNotFoundError:
                print("Файл не найден")
            except CorruptedSaveData:
                print("Файл поврежден и не может быть использован.")

        if username and password:
            print("Инициализация с авторизацией (юзернейм + пароль)")
            print(username, password)
            self.client = ApiClient(
                username=username,
                password=password,
            )
            self.client.log_in()
            print("Инициализация успешна")
            self.client.save_to_disk(session_file)
            print(f"Файл сессии сохранен в {session_file}")

            return

        raise ValueError("Нужно передать юзернейм + пароль или .instauto файл")

    def _get_followers_count(self, user_id: int) -> int:
        info_obj = Info(user_id=user_id)
        info = self.client.profile_info(info_obj)
        return int(info.get('follower_count'))

    def _get_following_count(self, user_id: int) -> int:
        info_obj = Info(user_id=user_id)
        info = self.client.profile_info(info_obj)
        return int(info.get('following_count'))

    def _get_user_id(self, username: str) -> int:
        return get_user_id_from_username(
            client=self.client,
            username=username,
        )

    def get_followers(self, username: str) -> list[int]:
        user_id = self._get_user_id(username=username)
        limit = self._get_followers_count(user_id=user_id)
        if limit > 900:
            limit = (len(read_accounts_from_csv("accounts.csv")) + 1) * 900
        print(f"Идет получение основных данных {limit} аккаунтов")
        followers = get_followers(
            client=self.client,
            user_id=user_id,
            limit=limit,
        )
        return list(map(lambda x: int(x.pk), followers))

    def get_following(self, username: str) -> list[int]:
        user_id = self._get_user_id(username=username)
        limit = self._get_following_count(user_id=user_id)
        if limit > 900:
            limit = (len(read_accounts_from_csv("accounts.csv")) + 1) * 900
        print(f"Идет получение основных данных {limit} аккаунтов")
        following = get_following(
            client=self.client,
            user_id=user_id,
            limit=limit,
        )
        return list(map(lambda x: int(x.pk), following))

    def get_user_info(self, user_id: int) -> Account:
        obj = Info(user_id=user_id)
        info = self.client.profile_info(obj=obj)

        login = info.get("username", None)
        followers = info.get("follower_count", 0)
        post = info.get("all_media_count", info.get("media_count", 0))
        email = info.get("public_email", None)
        phone = info.get("contact_phone_number", None)

        if not phone:
            phone = f'{info.get("public_phone_country_code", "")}{info.get("public_phone_country_code", "")}'
            if not phone:
                phone = None
            else:
                phone = '+' + phone

        if not info.get("is_private"):
            date = self._get_last_post_date(user_id=user_id)
        else:
            date = None

        return Account(
            login=login,
            followers=followers,
            post=post,
            email=email,
            phone_number=phone,
            date_of_last_post=date,
        )

    def _get_last_post_date(self, user_id: int) -> datetime | None:
        posts = retrieve_posts_from_user(
            client=self.client,
            limit=1,
            user_id=user_id,
        )

        return datetime.fromtimestamp(posts[0].taken_at) if posts else None
