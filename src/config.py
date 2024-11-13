from pydantic_settings import BaseSettings

class Config(BaseSettings):
    secret: str
    algorithm: str

    
class Config(BaseSettings):
    database:str
    user: str
    password: str
    host: str
    class Config:
        env_file = ".env"

config = Config()