# tests/conftest.py
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """Setup: Launch Chrome. Teardown: Quit + pause to avoid rate-limiting."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get("https://www.amazon.in")

    yield driver

    driver.quit()
    time.sleep(3)  # Pause between tests to avoid Amazon rate-limiting


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take a screenshot if a test fails."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"reports/failure_{item.name}.png"
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\n📸 Screenshot saved to: {screenshot_path}")
            except Exception:
                pass