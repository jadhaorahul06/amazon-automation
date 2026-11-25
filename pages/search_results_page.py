# pages/search_results_page.py
"""
Search Results Page Object - represents the page shown after searching.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class SearchResultsPage(BasePage):
    """Represents Amazon's search results page."""

    ALL_PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href*='/dp/']")

    def select_first_product(self):
        """
        Find the first product link with a real title, try to click it,
        and if that opens in a new tab OR doesn't navigate, force-navigate
        to the /dp/ URL directly.
        Returns ProductPage.
        """
        # Wait for product links to appear
        self.wait.until(lambda d: len(d.find_elements(*self.ALL_PRODUCT_LINKS)) > 0)

        links = self.driver.find_elements(*self.ALL_PRODUCT_LINKS)

        # Find the first link with a real title (long text)
        product_url = None
        for link in links:
            try:
                href = link.get_attribute("href") or ""
                text = (link.text or "").strip()

                if "/dp/" not in href:
                    continue
                if len(text) < 10:
                    continue

                # Extract the canonical product URL (up to the ASIN)
                # e.g. https://www.amazon.in/Some-Book-Name/dp/B0CHX1W1XY/ref=...
                parts = href.split("/dp/")
                if len(parts) == 2:
                    asin = parts[1].split("/")[0].split("?")[0]
                    product_url = f"https://www.amazon.in/dp/{asin}"
                    break
            except Exception:
                continue

        if not product_url:
            raise Exception("No product URL with /dp/ and visible title found.")

        # Attempt JS click first (works if target is same tab)
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, f"a[href*='{product_url.split('/dp/')[1]}']")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.3)
            self.driver.execute_script("arguments[0].click();", element)

            # Wait up to 3 seconds for URL change
            for _ in range(6):
                time.sleep(0.5)
                if "/dp/" in self.driver.current_url:
                    break
        except Exception:
            pass

        # If we're still not on a product page, force-navigate
        if "/dp/" not in self.driver.current_url:
            self.driver.get(product_url)
            self.wait.until(lambda d: "/dp/" in d.current_url)

        from pages.product_page import ProductPage
        return ProductPage(self.driver)