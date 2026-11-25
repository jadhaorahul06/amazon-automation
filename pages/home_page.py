# pages/home_page.py
"""
Home Page Object - represents Amazon's home page.
Contains the search box, search button, and search action.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Represents Amazon's home page."""

    # --- Locators ---
    # Each locator is a (By.STRATEGY, "value") tuple
    SEARCH_BOX = (By.ID, "twotabsearchtextbox")
    SEARCH_BUTTON = (By.ID, "nav-search-submit-button")

    # --- Actions ---
    def search_for(self, product_name):
        """
        Type product name in search box, click search.
        Returns the SearchResultsPage object.
        """
        self.send_keys(self.SEARCH_BOX, product_name)
        self.click(self.SEARCH_BUTTON)

        # Import here to avoid circular import at module load time
        from pages.search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver)


    SIGN_IN_BUTTON = (By.ID, "nav-link-accountList")


    def click_sign_in(self):
        """Click the Sign In button. Returns LoginPage."""
        self.click(self.SIGN_IN_BUTTON)

        from pages.login_page import LoginPage
        return LoginPage(self.driver)