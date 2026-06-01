# QA-Automation-Portfolio

## 📌 Overview
UI automation framework using:
- Playwright
- pytest
- Allure reporting

## ⚙️ Tech Stack
- Python 3.14+
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
<!-- 
## 🔄 CI/CD

- Runs pytest
- Generates Allure results
- Uploads artifacts

## 📌 Conventions -->