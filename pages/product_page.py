# pages/product_page.py
"""
Product Page Object - represents an individual product detail page.
Contains the logic to add a product to the cart.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Represents an Amazon product detail page."""

    # --- Locators ---
    # Find any button or input that contains the text "Add to cart" (case insensitive)
    ADD_TO_CART_BUTTON = (
        By.XPATH,
        "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart') or contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add to cart')]"
    )

    CART_ICON = (By.ID, "nav-cart")
    # Product price on the detail page
    PRICE_LOCATOR = (
        By.CSS_SELECTOR,
        "span.a-price span.a-offscreen, "
        ".priceToPay span.a-offscreen, "
        "#priceblock_ourprice"
    )

    # --- Actions ---
    def add_to_cart(self):
        """Click the Add to Cart button."""
        self.click(self.ADD_TO_CART_BUTTON)

    def get_price(self):
        """Return the visible price text (e.g. '₹1,099.00')."""
        try:
            text = self.get_text(self.PRICE_LOCATOR)
            return text.strip()
        except Exception:
            return ""
    def go_to_cart(self):
        """Click the cart icon to view the cart. Returns CartPage."""
        self.click(self.CART_ICON)

        from pages.cart_page import CartPage
        return CartPage(self.driver)