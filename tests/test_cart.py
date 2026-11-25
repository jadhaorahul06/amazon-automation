# pages/cart_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CartPage(BasePage):
    """Represents Amazon's shopping cart page."""

    # --- Locators ---
    PAGE_HEADING = (By.CSS_SELECTOR, "h1")

    # A more generic locator for the cart items
    CART_ITEMS = (By.CSS_SELECTOR, "div.sc-list-item")

    # The Delete button
    DELETE_BUTTON = (By.CSS_SELECTOR, "input[value='Delete'], span[data-action='delete']")

    # --- Actions ---
    def get_heading_text(self):
        return self.get_text(self.PAGE_HEADING)

    def get_cart_item_count(self):
        """Wait for cart items to appear, then return the count."""
        try:
            # This line forces Selenium to wait until at least ONE item is visible.
            # If the cart is empty, it will wait 5 seconds and then return 0.
            self.wait.until(EC.presence_of_element_located(self.CART_ITEMS))
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except Exception:
            # If it times out, the cart is likely empty
            return 0

    def remove_first_item(self):
        """Clicks the 'Delete' button on the first item in the cart."""
        self.click(self.DELETE_BUTTON)