import pydantic_settings
import os

#below shows use of pydantic to validate env variables
class Settings(pydantic_settings.BaseSettings):
    DB_HOSTNAME: str 
    DB_PORT: str  #old code had the url as a string
    DB_PASSWORD: str
    DB_NAME: str
    DB_USERNAME: str
    class Config:
        env_file = ".env"

if __name__ == "__main__":
    settings = Settings()