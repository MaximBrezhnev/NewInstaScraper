from pydantic_settings import BaseSettings, SettingsConfigDict

from utils import resource_path


class Settings(BaseSettings):
    ig_username: str
    ig_password: str
    filename: str
    session_file: str

    model_config = SettingsConfigDict(
        env_file=resource_path('.env'),
        env_file_encoding='utf-8',
    )

    # class Config:
    #     env_file = '.env'
    #     # env_file = resource_path('.env')
    #     env_file_encoding = 'utf-8'


config = Settings()
