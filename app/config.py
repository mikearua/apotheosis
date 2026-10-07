from pydantic_settings import BaseSettings


# THE DATATYPE OF THE ENV VARS WE NEED TO BE SAVED IN A SCHEMA
class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    second_database_name: str
    class Config:
        env_file = ".env" #IMPORTING THE ENV VAR
    
settings = Settings()  #AN INSTANCE OF THE CLASS SETTINGS

#
