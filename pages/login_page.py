# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Represents the Amazon Sign-In page."""

    # --- Locators ---
    # Find the FIRST visible input field on the page.
    # This works regardless of what Amazon names the ID or Type.
    EMAIL_INPUT = (
        By.XPATH,
        "(//input[@type='text' or @type='email' or @type='tel' or @name='email' or @id='ap_email'])[1]"
    )

    # The "Continue" button is usually an input or a button with "continue" in the ID or type="submit"
    CONTINUE_BUTTON = (
        By.XPATH,
        "//input[contains(@id, 'continue')] | //button[contains(@id, 'continue')] | //input[@type='submit']"
    )

    # --- Actions ---
    def enter_email(self, email):
        """Type the email into the input field."""
        self.send_keys(self.EMAIL_INPUT, email)

    def click_continue(self):
        """Click the Continue button."""
        self.click(self.CONTINUE_BUTTON)