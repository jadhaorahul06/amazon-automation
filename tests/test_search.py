# tests/test_search.py
import pytest
from pages.home_page import HomePage

# We define a list of items to search for
SEARCH_TERMS = ["wireless headphones", "python book", "mechanical keyboard"]


@pytest.mark.parametrize("search_term", SEARCH_TERMS)
def test_search_and_add_to_cart(driver, search_term):
    """
    Test Flow:
    1. Open Amazon
    2. Search for a product (parameterized)
    3. Click the first result
    4. Add it to the cart
    5. Verify we are on the cart page
    """
    home_page = HomePage(driver)

    # The search_term is injected by PyTest
    search_results = home_page.search_for(search_term)
    product_page = search_results.select_first_product()
    product_page.add_to_cart()
    cart_page = product_page.go_to_cart()

    assert "cart" in driver.current_url.lower(), f"Failed to add {search_term} to cart!"