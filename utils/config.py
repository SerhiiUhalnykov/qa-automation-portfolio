from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    base_url: str
    api_url: str
    artifacts_dir: str = "artifacts"
    browser: str = "chromium"

    user_stan: str = ""
    pass_stan: str = ""
    user_admin: str = ""
    pass_admin: str = ""
    user_api: str = ""
    pass_api: str = ""


settings = Settings()  # type: ignore[call-arg]
