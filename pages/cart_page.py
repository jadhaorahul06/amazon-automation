# pages/cart_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class CartPage(BasePage):
    """Represents Amazon's shopping cart page."""
    def get_first_item_price(self):
        """Return the price text of the first item in the cart."""
        try:
            text = self.get_text(self.FIRST_ITEM_PRICE)
            return text.strip()
        except Exception:
            return ""
    # --- Locators ---
    PAGE_HEADING = (By.CSS_SELECTOR, "h1")
    CART_ITEMS = (By.CSS_SELECTOR, "div.sc-list-item")
    DELETE_BUTTON = (By.CSS_SELECTOR, "input[value='Delete'], span[data-action='delete']")

    # Price of the first item inside the cart (the subtotal line is separate)
    FIRST_ITEM_PRICE = (
        By.CSS_SELECTOR,
        "div.sc-list-item span.a-price span.a-offscreen, "
        "div.sc-list-item .sc-product-price"
    )

    # The "+" button to increase quantity (Amazon uses a span/button now)
    QUANTITY_INCREASE_BTN = (
        By.CSS_SELECTOR,
        "button[data-a-selector='increment'], "
        "span[data-action='a-stepper-increment'], "
        "button[aria-label='Increase Quantity'], "
        "input[aria-label*='+']"
    )

    # The "Subtotal (X items)" text — try multiple selectors
    SUBTOTAL_TEXT = (
    By.CSS_SELECTOR, "#sc-subtotal-label-activecart, #sc-subtotal-label-buybox, span[id*='subtotal-label']")

    # --- Actions ---
    def get_heading_text(self):
        return self.get_text(self.PAGE_HEADING)

    def get_cart_item_count(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.CART_ITEMS))
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except Exception:
            return 0

    def remove_first_item(self):
        """Clicks the 'Delete' button on the first item in the cart."""
        self.click(self.DELETE_BUTTON)

    def increase_quantity(self):
        """Click the '+' button to increase quantity by 1."""
        self.click(self.QUANTITY_INCREASE_BTN)
        # Wait for the subtotal to update (Amazon reloads via AJAX)
        time.sleep(3)

    def get_subtotal_text(self):
        """Return the subtotal text (e.g., 'Subtotal (2 items): ...')"""
        try:
            return self.get_text(self.SUBTOTAL_TEXT)
        except Exception:
            return ""