# QA-Automation-Portfolio
[![Smoke tests](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/smoke.yml/badge.svg)](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/smoke.yml)

[![Regression tests](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/regression.yml/badge.svg)](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/regression.yml)

![Python](https://img.shields.io/badge/python-3.1x-blue)
![Pytest](https://img.shields.io/badge/pytest-9.x-brightgreen)
![Playwright](https://img.shields.io/badge/playwright-1.6-brightgreen)
![Allure](https://img.shields.io/badge/allure-2.42.0-brightgreen)

## Lastest Published Report:
[Regression tests pipeline latest report](https://serhiiuhalnykov.github.io/qa-automation-portfolio/)

## 📌 Overview
UI automation framework using Playwright with pytest and Allure for reporting
on a public website ![herokuapp](https://the-internet.herokuapp.com) as a test subject.

## ⚙️ Tech Stack
- Python 3.10+
- Playwright
- Allure
- pytest
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
# Playwright browsers
python -m playwright install --with-deps
# Node dependencies (optional to gen Allure reports)
npm ci
# Create and fill file for env variables
cp .env.example .env
```

## ▶️ Running Tests
```bash
pytest --alluredir=allure-results
```
## 📊 Allure Reports
```bash
npx allure generate allure-results -o allure-report --clean
npx allure serve allure-report
```
<!-- ## 🧪 Test Structure -->
## 📁 Project Structure
```
├── .github
│   └─── workflows    # ci pipelines
│
├── fixtures/         # separated fixtures
├── pages/            # page objects
├── tests/            # test cases
├── utils/            # helper modules
|
├── allure-report/    # generated Allure HTML report
├── allure-results/   # generated Allure raw results
├── artifacts/        # generated for screenshots/traces on fail
|
├── conftest.py       # shared pytest fixtures/hooks
├── pytest.ini        # pytest config
├── .env              # environment variables
|
├── package-lock.json # npm dependencies for Allure Reporting
├── package.json
├── requirements.txt  # python dependencies
```
## 🐞 Debugging
If test fails:

1. Check Allure report
2. Open screenshot attachment
3. Open trace.zip
4. Check console logs

## 🔄 CI/CD
The project uses GitHub Actions for automated testing and reporting.

### Workflows
* Pull Requests / Push to main
    * Runs smoke tests
    * Executes Playwright tests (Chromium)
    * Generates test artifacts on fail and allure results
* Nightly Regression
    * Runs full regression suite on schedule
    * Executes cross-browser matrix (Chromium, Firefox, WebKit)
    * Generates, merges and deploys Allure report

### Environment Setup
Configuration is managed via .env locally and GitHub Actions variables in CI.