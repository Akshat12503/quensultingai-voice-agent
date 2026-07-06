from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    airtable_api_key: str
    airtable_base_id: str
    airtable_table_name: str = "Appointments"

    brevo_api_key: str

    retell_webhook_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()