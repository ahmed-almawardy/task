import os

class Config:
    DEBUG: bool = os.environ.get('APP_DEBUG')
    HOST: str = os.environ.get('APP_HOST')
    PORT: int = os.environ.get('APP_PORT')
    DATABASE_URI: str \
        = f'postgresql://{os.environ.get("POSTGRES_USER")}' \
          f':{os.environ.get("POSTGRES_PASSWORD")}' \
          f'@{os.environ.get("DB_HOST")}:' \
          f'{os.environ.get("DB_PORT")}/' \
          f'{os.environ.get("POSTGRES_DB")}'

