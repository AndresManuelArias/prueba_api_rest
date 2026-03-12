from .db import DatabaseSettings


class Settings(DatabaseSettings):
    project_name: str = "api_rest"
    debug: bool = False
