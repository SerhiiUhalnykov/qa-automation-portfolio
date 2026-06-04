# QA-Automation-Portfolio
[![Smoke tests](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/SerhiiUhalnykov/qa-automation-portfolio/actions/workflows/tests.yml)

![Python](https://img.shields.io/badge/python-3.1x-blue)
![Pytest](https://img.shields.io/badge/pytest-9.x-green)
![Playwright](https://img.shields.io/badge/playwright-1.6-brightgreen)
![Allure](https://img.shields.io/badge/allure-reporting-orange)

## 📌 Overview
UI automation framework using:
- Playwright
- pytest
- Allure reporting

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

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

playwright install
npm install allure-commandline --save-dev
```

## ▶️ Running Tests
```bash
pytest
```
## 📊 Allure Reports
```bash
npx allure generate allure-results -o allure-report --clean
npx allure serve allure-results
```
<!-- ## 🧪 Test Structure -->
## 📁 Project Structure
```
├── pages/          # page objects
├── tests/          # test cases
├── utils/          # helper modules
|
├── allure-report/  # generated Allure HTML report
├── allure-results/ # generated Allure raw results
├── artifacts/      # generated for screenshots/traces on fail
|
├── conftest.py     # shared pytest fixtures/hooks
├── pytest.ini      # pytest config
```
## 🐞 Debugging

If test fails:

1. Check Allure report
2. Open screenshot attachment
3. Open trace.zip
4. Check console logs

## 🔄 CI/CD

The project uses GitHub Actions to automatically validate changes on every push and pull request.

### Pipeline

1. Checkout repository
2. Set up Python environment
3. Install project dependencies
4. Install Playwright browsers
5. Run smoke tests
6. Collect Allure results
7. Upload test artifacts

### Artifacts on Failure

- Playwright screenshots
- Playwright traces
- Allure test results