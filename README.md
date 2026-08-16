# Playwright Automation Testing Practice - Automation Exercise

This repository contains an end-to-end Test Automation Framework built from scratch using **Python**, **Playwright** and **Pytest**. 

The target system under test is the e-commerce practice platform: [Automation Exercise](https://automationexercise.com/).

---

## 🚀 Key Highlights & Architecture

* **Page Object Model:** Clean separation of concerns between UI Locators, Page Actions and Test Assertions.
* **Data-Driven Testing:** Test cases dynamically read inputs from an external Excel file (`.xlsx`) via `openpyxl`. Tests can be selectively enabled or disabled using the `Enabled` column.
* **Fail-Fast Error Handling:** Quickly captures native HTML5 tooltips and server-side validation error messages without unnecessary wait times.
* **Automated Data Teardown:** Test cases creating new accounts automatically clean up after themselves to maintain a pristine database state across multiple runs.
* **Robust Reporting & Artifacts:** Integrated with `pytest-html` for self-contained HTML test reports and hooks for automated full-page screenshots upon test failure.

---

## 📁 Project Directory Structure

```text
playwright-automationexercise/
├── config/
│   └── config.py             # Environment configurations, Base URL, timeouts, slow_mo settings
├── data/
│   └── test_data.xlsx        # Excel test data sheets
├── locators/
│   ├── login_locators.py     # UI selectors for Authentication pages
│   ├── register_locators.py  # UI selectors for Signup pages
│   └── search_locators.py    # UI selectors for Search pages
├── pages/
│   ├── base_page.py          # Base wrapper for Playwright actions
│   ├── login_page.py         # Page Object for Login interactions
│   ├── register_page.py      # Page Object for Registration workflows
│   └── search_page.py        # Page Object for Product search
├── tests/
│   ├── test_login.py         # Test scenarios for User Login
│   ├── test_register.py      # Test scenarios for User Registration
│   └── test_search.py        # Test scenarios for Product Search
├── utils/
│   ├── excel_utils.py        # Utility to parse Excel sheets into Python dictionaries
│   └── logger.py             # Custom logger configuration for execution logs
├── conftest.py               # Fixtures for browsers (Chrome, Firefox, Edge) & failure hooks
├── pytest.ini                # Pytest execution settings and report options
├── .gitignore                # Rules for excluding cache, environments, logs, reports
└── README.md                 # Project documentation
```

---

## 💻 Prerequisites & Setup

### 1. Prerequisites
* **Python 3.10+** installed on your system.
* **Git** installed.

### 2. Clone Repository
```bash
git clone https://github.com/NTKTien/playwright-automationexercise.git
cd playwright-automationexercise
```

### 3. Set Up Virtual Environment

* **On Windows (PowerShell / Command Prompt):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies & Browsers
```bash
pip install pytest pytest-playwright openpyxl pytest-html python-dotenv
playwright install
```

---

## 🛠️ Test Execution Guide

### 1. Run the Entire Test Suite
Executes all test modules sequentially across supported browsers and produces an HTML report:
```bash
pytest
```

### 2. Run Specific Test Modules
* **Register Module:**
  ```bash
  pytest tests/test_register.py
  ```
* **Login Module:**
  ```bash
  pytest tests/test_login.py
  ```
* **Search Module:**
  ```bash
  pytest tests/test_search.py
  ```

### 3. Run with UI Display (Headed Mode)
By default, tests run in headless mode. To watch browser interactions:

* **Windows PowerShell:**
  ```powershell
  $env:HEADLESS="false"; pytest tests/test_login.py
  ```
* **macOS / Linux:**
  ```bash
  HEADLESS=false pytest tests/test_login.py
  ```

### 4. Run in Slow Motion (Debugging)
Slows down Playwright execution by a specific number of milliseconds per action (e.g., 500ms):

* **Windows PowerShell:**
  ```powershell
  $env:SLOW_MO="500"; $env:HEADLESS="false"; pytest tests/test_search.py
  ```
* **macOS / Linux:**
  ```bash
  SLOW_MO=500 HEADLESS=false pytest tests/test_search.py
  ```

---

## 📊 Test Reports & Failure Artifacts

* **HTML Report:** Generated after execution at:
  ```text
  reports/report.html
  ```
  *(Can be opened directly in any web browser).*

* **Failure Screenshots:** Automatically captured upon any test failure and stored in:
  ```text
  screenshots/FAIL_<TestCaseID>_<Browser>_<Timestamp>.png
  ```