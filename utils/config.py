import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "")
API_URL: str = os.getenv("API_URL", "")

ARTIFACTS_DIR: str = os.getenv("ARTIFACTS_DIR", "artifacts")

BROWSER_NAME: str = os.getenv("BROWSER", "chromium")


class Users:
    STAN_USER: str = os.getenv("USER_STAN", "")
    STAN_PASS: str = os.getenv("PASS_STAN", "")

    ADMIN_USER: str = os.getenv("USER_ADMIN", "")
    ADMIN_PASS: str = os.getenv("PASS_ADMIN", "")

    API_USER: str = os.getenv("API_USER", "")
    API_PASS: str = os.getenv("API_PASS", "")
