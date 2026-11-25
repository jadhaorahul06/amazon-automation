# tests/test_quantity.py
from pages.home_page import HomePage


def test_change_quantity(driver):
    """
    Test Flow:
    1. Add a product to cart
    2. Go to cart, verify quantity is 1
    3. Click the + button to increase quantity to 2
    4. Verify subtotal reflects 2 items
    """
    home_page = HomePage(driver)

    # Add a product
    search_results = home_page.search_for("wireless headphones")
    product_page = search_results.select_first_product()
    product_page.add_to_cart()
    cart_page = product_page.go_to_cart()

    # Verify initial subtotal says 1 item
    initial_text = cart_page.get_subtotal_text()
    print(f"\nInitial subtotal: {initial_text}")
    assert "1" in initial_text, f"Expected 1 item, got: '{initial_text}'"

    # Click "+" button to increase quantity
    cart_page.increase_quantity()

    # Verify subtotal says 2 items
    updated_text = cart_page.get_subtotal_text()
    print(f"\nUpdated subtotal: {updated_text}")
    assert "2" in updated_text, f"Expected 2 items, got: '{updated_text}'"