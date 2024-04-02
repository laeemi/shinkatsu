from typing import Optional, Self

from pydantic import RedisDsn, model_validator
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    TOKEN: str
    ADMIN: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: Optional[RedisDsn] = None

    @model_validator(mode="before")
    def redis_postgres_db_url(self) -> Self:
        self["REDIS_URL"] = RedisDsn.build(scheme="redis", host=self["REDIS_HOST"], port=int(self["REDIS_PORT"]))
        return self


bot_settings = BotSettings()

if __name__ == "__main__":
    print(bot_settings.TOKEN)
