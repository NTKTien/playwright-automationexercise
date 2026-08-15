import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, DEFAULT_TIMEOUT, HEADLESS, SLOW_MO

SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]

@pytest.fixture(params=SUPPORTED_BROWSERS, scope="function")
def driver_setup(request):
    browser_type_name = request.param
    with sync_playwright() as p:
        if browser_type_name == "chrome":
            browser = p.chromium.launch(headless=HEADLESS, channel="chrome", slow_mo=SLOW_MO)
        elif browser_type_name == "edge":
            browser = p.chromium.launch(headless=HEADLESS, channel="msedge", slow_mo=SLOW_MO)
        elif browser_type_name == "firefox":
            browser = p.firefox.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        else:
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)

        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        
        # Đợi DOM load thay vì đợi tất cả ảnh/script
        page.goto(BASE_URL, wait_until="domcontentloaded")

        yield {"page": page, "browser_name": browser_type_name}

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            test_id = getattr(request.node, "test_id", request.node.name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/FAIL_{test_id}_{browser_type_name}_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)

        context.close()
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)