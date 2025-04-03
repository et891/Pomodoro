from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_TOKEN_ID:str = "fes324fsd2342j324j32j324joi34j2"
    sqlite3_db_name:str ="pomodoro.sqlite"
    JWT_SECRET_KEY: str = "secret_key"
    JWT_DECODE_ALGORITHM: str = "HS256"