# QA-Automation-Portfolio
[![Smoke tests](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/smoke.yml/badge.svg)](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/smoke.yml)

[![Regression tests](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/regression.yml/badge.svg)](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/regression.yml)

![Python](https://img.shields.io/badge/python-3.1x-blue)
![Pytest](https://img.shields.io/badge/pytest-9.x-brightgreen)
![Pydantic](https://img.shields.io/badge/pydantic-2.x-brightgreen)
![Playwright](https://img.shields.io/badge/playwright-1.6-brightgreen)
![Allure](https://img.shields.io/badge/allure-2.42.0-brightgreen)

## Lastest Published Report:
[Regression tests pipeline latest report](https://serhiiuhalnykov.github.io/qa-automation-portfolio/)

## 📌 Overview
Combined UI and API automation framework using:
- **UI**: Playwright + pytest + Page Object Model, targeting the public site [herokuapp](https://the-internet.herokuapp.com)
- **API**: requests + pytest + Pydantic schema validation, targeting the public mock API [DummyJSON](https://dummyjson.com)

## ⚙️ Tech Stack
- Python 3.10+
- Playwright
- pytest
- Pydantic
- requests
- Faker
- Allure
- python-dotenv

## 🚀 Setup
```bash
git clone <repo>
cd project
# Python virtual environment
python -m venv .venv
source .venv/bin/activate
# Python dependencies
pip install -r requirements.txt
# Playwright browsers (UI tests only)
python -m playwright install --with-deps
# Create and fill file for env variables
cp .env.example .env
```

> **Note:** Allure CLI is required separately to generate/view HTML reports locally — install via [Allure's official instructions](https://allurereport.org/docs/install/) (Homebrew, Scoop, npm `-g`, or standalone).

## ▶️ Running Tests
```bash
pytest                  # everything
pytest -m "not api"     # UI only
pytest -m "api"         # API only
pytest -m "smoke"       # smoke subset
```
## 📊 Allure Reports
```bash
allure generate allure-results -o allure-report --clean
allure serve allure-report
```
<!-- ## 🧪 Test Structure -->
## 📁 Project Structure
```
├── .github
│   └── workflows    # ci pipelines (smoke, regression)
│
├── api/              # API clients (BaseClient, AuthClient, PostsClient, etc.)
├── models/           # Pydantic request/response models
├── pages/            # UI page objects
├── tests/            # test cases
│   └── ui/          # UI test cases + conftest
│   └── api/          # API test cases + conftest
├── utils/            # helper modules (config, logger, assertions)
|
├── allure-results/   # generated Allure raw results
├── allure-report/    # generated Allure HTML report
├── artifacts/        # generated screenshots/traces (UI) and reponse dumps (API) on fail
|
├── conftest.py       # shared pytest fixtures/hooks
├── pytest.ini        # pytest config
├── .env              # environment variables
|
├── requirements.txt  # python dependencies
```
## 🐞 Debugging
**UI failures:**
1. Check Allure report
2. Open screenshot attachment
3. Open trace.zip
4. Check console logs

**API failures:**
1. Check Allure report
2. Open attached request/response JSON (URL, method, status, body)
3. Check console logs

## 🔄 CI/CD
The project uses GitHub Actions for automated testing and reporting.

### Workflows
* Pull Requests / Push to main
    * Runs smoke-marked tests (UI on Chromium + API)
    * Generates test artifacts on fail and Allure results
* Nightly Regression
    * Runs full regression suite on schedule
    * UI: cross-browser matrix (Chromium, Firefox, WebKit)
    * API: single dedicated job (browser-independent)
    * Merges results from all jobs, generates and deploys Allure report with history

### Environment Setup
Configuration is managed via `.env` locally and GitHub Actions variables in CI.

### Additional Info:
> **Note:** API tests target [DummyJSON](https://dummyjson.com), a public mock REST API. Write operations (`POST`/`PUT`/`PATCH`/`DELETE`) are simulated by the API and do not persist server-side — responses reflect expected behavior but won't be retrievable on subsequent requests.

> **Note:** Allure reports for API tests may display test credentials/tokens in plaintext. This is intentional — all test data uses public mock APIs (DummyJSON) with publicly documented, non-sensitive credentials.