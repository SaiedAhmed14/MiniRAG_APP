from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_KEY:str

    #!File uploading settings
    FILE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_CHUNK_SIZE:int

    #^database settings
    MONGODB_URL:str
    MONGODB_DATABASE:str

    class config :
        env_file=".env"
def get_settings():
    return Settings()    