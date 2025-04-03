from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "fes324fsd2342j324j32j324joi34j2"
    sqlite3_db_name: str = "pomodoro.sqlite"
    JWT_SECRET_KEY: str = "secret_key"
    JWT_DECODE_ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str
    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'

    model_config = SettingsConfigDict(env_file=".local.env")

    @property
    def google_auth_url(self) -> str:
        return (
            "https://accounts.google.com/o/oauth2/auth"
            f"?response_type=code"
            f"&client_id={self.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={self.GOOGLE_REDIRECT_URI}"
            f"&scope=openid%20email%20profile"
            f"&access_type=offline"
            f"&prompt=consent"
        )

    @property
    def yandex_auth_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}"
