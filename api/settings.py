from pydantic_settings import BaseSettings
from pydantic import Extra
        
class MariaSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    database: str
    
    class Config:
        extra = "allow"
        env_prefix = 'MARIA_'
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
class MqttSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    
    class Config:
        extra = "allow"
        env_prefix = 'MQTT_'
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False    
    
class Settings(BaseSettings):
    key: str
    
    class Config:
        extra = "allow"
        env_prefix = 'APP_'
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False