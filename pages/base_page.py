# pages/base_page.py
"""
Base Page Object - parent class for all pages.
Contains reusable actions every page needs: find, click, type, get text.
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # max 10-second wait

    # ------------------------------------------------------------------
    # Internal helper: run an action on an element, retrying on stale.
    # Amazon re-renders heavily; the element we grabbed 200ms ago may be
    # a detached DOM node by the time we call .clear() / .click().
    # ------------------------------------------------------------------
    def _retry_on_stale(self, action, locator, *args, retries=3):
        last_exc = None
        for _ in range(retries):
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                return action(element, *args)
            except StaleElementReferenceException as e:
                last_exc = e
                time.sleep(0.3)  # let the re-render settle
        raise last_exc

    # ------------------------------------------------------------------
    # Basic finders
    # ------------------------------------------------------------------
    def find_element(self, locator):
        """Wait until element is present in DOM, then return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Wait until at least one element is present, return list."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    # ------------------------------------------------------------------
    # Click
    # ------------------------------------------------------------------
    def click(self, locator):
        """Wait until element is visible + clickable, scroll, then click.
        Falls back to JS click if intercepted, and retries on stale."""
        def _do(element):
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            time.sleep(0.2)
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)
            return True

        return self._retry_on_stale(_do, locator)

    # ------------------------------------------------------------------
    # Send keys
    # ------------------------------------------------------------------
    def send_keys(self, locator, text):
        """Clear field and type text, retrying on stale element."""
        def _do(element):
            element.clear()
            element.send_keys(text)
            return True

        return self._retry_on_stale(_do, locator)

    # ------------------------------------------------------------------
    # Read helpers
    # ------------------------------------------------------------------
    def get_text(self, locator):
        """Return visible text of an element (retries on stale)."""
        def _do(element):
            return element.text

        return self._retry_on_stale(_do, locator)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url