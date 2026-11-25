# tests/test_login.py
from pages.home_page import HomePage


def test_navigate_to_login(driver):
    """Test that we can reach the login page and type an email."""
    home_page = HomePage(driver)

    # Click Sign In
    login_page = home_page.click_sign_in()

    # Enter a fake email
    login_page.enter_email("testuser@example.com")

    # Verify we are on the email entry page
    assert "signin" in driver.current_url.lower() or "ap/signin" in driver.current_url.lower()