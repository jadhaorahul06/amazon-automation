# tests/test_price.py
from pages.home_page import HomePage


def test_price_matches_between_product_and_cart(driver):
    home_page = HomePage(driver)

    # Navigate to search results
    search_results = home_page.search_for("python book")

    # --- DEBUG: List all /dp/ links found ---
    from selenium.webdriver.common.by import By
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/dp/']")
    print(f"\n\n=== FOUND {len(links)} PRODUCT LINKS ===")
    for i, link in enumerate(links[:5]):  # show first 5
        href = link.get_attribute("href")
        text = link.text[:60] if link.text else "(no text)"
        displayed = link.is_displayed()
        print(f"Link {i}: displayed={displayed}, href={href}")
        print(f"         text='{text}'")
    print("=========================================\n")

    # Now try to click the first product
    product_page = search_results.select_first_product()

    # --- DEBUG: Show where we ended up ---
    print(f"\n>>> Current URL: {driver.current_url}")
    print(f">>> Page title: {driver.title}")

    # Verify we're on a product detail page
    assert "/dp/" in driver.current_url, \
        f"Expected product page, but got: {driver.current_url}"