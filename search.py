"""
Selenium automation: Search for a product and add it to the cart.

Requirements:
  - Python 3.8+
  - pip install selenium webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
BASE_URL       = "https://adnabu-store-assignment1.myshopify.com"
STORE_PASSWORD = "AdNabuQA"
SEARCH_TERM    = "snowboard"
PRODUCT_NAME   = "The Videographer Snowboard"
TIMEOUT        = 10  # seconds


# ─────────────────────────────────────────────
# BROWSER SETUP
# ─────────────────────────────────────────────
def create_driver() -> webdriver.Chrome:
    """Return a configured Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


# ─────────────────────────────────────────────
# STEP HELPERS
# ─────────────────────────────────────────────
def log(step: int, message: str) -> None:
    print(f"\n[Step {step}] {message}")

def ok(message: str) -> None:
    print(f"  ✓ {message}")

def fail(message: str) -> None:
    print(f"  ✗ {message}")


# ─────────────────────────────────────────────
# PAGE ACTIONS
# ─────────────────────────────────────────────
def login(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    """Navigate to the password-protected store and authenticate."""
    log(1, "Logging in to store")

    driver.get(f"{BASE_URL}/password")

    password_input = wait.until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(STORE_PASSWORD)
    ok("Password entered")

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    submit_btn.click()

    # Confirm we've left the password page
    wait.until(EC.url_changes(f"{BASE_URL}/password"))
    ok("Logged in successfully")


def go_home(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    """Load the store home page."""
    log(2, "Loading home page")

    driver.get(BASE_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    ok("Home page loaded")


def search_product(driver: webdriver.Chrome, wait: WebDriverWait, term: str) -> None:
    """Navigate directly to search results for *term*."""
    log(3, f"Searching for '{term}'")

    driver.get(f"{BASE_URL}/search?q={term}")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    ok(f"Search results page loaded")


def click_product(wait: WebDriverWait, product_title: str) -> None:
    """Click the product link that exactly matches *product_title*."""
    log(4, f"Opening product: {product_title}")

    product_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, product_title))
    )
    product_link.click()

    # Product page signals readiness when the add-to-cart button is present
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[name='add']"))
    )
    ok("Product page loaded")


def add_to_cart(wait: WebDriverWait) -> None:
    """Click the Add-to-Cart button. Does NOT wait for the drawer — caller handles that."""
    log(5, "Adding product to cart")

    add_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='add']"))
    )
    add_btn.click()
    ok("'Add to cart' clicked")


def dismiss_cart_dialog(wait: WebDriverWait) -> None:
    """After Add to Cart, close the auto-opened dialog via the X button."""
    log(6, "Dismissing cart dialog (X button)")

    # Wait for the dialog to appear first
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
    )
    ok("Cart dialog appeared")

    close_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
    )
    close_btn.click()

    # Confirm dialog is fully gone before proceeding
    wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
    )
    ok("Cart dialog dismissed")


def verify_cart_badge(wait: WebDriverWait) -> None:
    """Verify 1: Cart badge count updates to 1 after adding product."""
    log(6, "Verify 1 — Cart badge updates to 1")

    badge = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#cart-icon-bubble"))
    )
    badge_text = badge.text.strip()

    if "1" in badge_text:
        ok(f"Cart badge shows 1")
    else:
        fail(f"Cart badge shows unexpected value: '{badge_text}'")


def verify_product_in_cart(wait: WebDriverWait, product_name: str) -> None:
    """Verify 2: Click the cart icon to open the drawer, confirm product name is listed."""
    log(8, f"Verify 2 — Open cart drawer and confirm '{product_name}' is listed")

    # Click the cart icon in the header to open the drawer
    cart_icon = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']"))
    )
    cart_icon.click()

    # Wait for the drawer to open
    drawer = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
    )
    ok("Cart drawer opened")

    if product_name in drawer.text:
        ok(f"'{product_name}' found in cart drawer")
    else:
        fail(f"'{product_name}' NOT found — drawer contents:\n{drawer.text[:300]}")


def close_cart(wait: WebDriverWait) -> None:
    """Verify 3: Close the cart drawer via the X button and confirm it disappears."""
    log(9, "Verify 3 — Close cart drawer")

    close_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
    )
    close_btn.click()

    wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
    )
    ok("Cart drawer closed")


# ─────────────────────────────────────────────
# MAIN TEST RUNNER
# ─────────────────────────────────────────────
def run_test() -> bool:
    """
    End-to-end scenario:

      1. Login
      2. Go to home page
      3. Search for product
      4. Click product from results
      5. Click Add to cart
      6. Close the auto-opened cart dialog (X button)
      --- Verifications ---
      7. Verify 1: Cart badge updates to 1
      8. Verify 2: Navigate to /cart → product name visible in drawer
      9. Verify 3: Close the cart drawer

    Returns True on success, False on failure.
    """
    driver = create_driver()
    wait   = WebDriverWait(driver, TIMEOUT)

    print("\n" + "=" * 60)
    print("TEST: Search product and add to cart")
    print("=" * 60)

    try:
        login(driver, wait)                                    # Step 1
        go_home(driver, wait)                                  # Step 2
        search_product(driver, wait, SEARCH_TERM)              # Step 3
        click_product(wait, PRODUCT_NAME)                      # Step 4
        add_to_cart(wait)                                      # Step 5
        dismiss_cart_dialog(wait)                              # Step 6 — close auto-opened dialog
        verify_cart_badge(wait)                                # Verify 1: badge shows 1
        verify_product_in_cart(wait, PRODUCT_NAME)            # Verify 2: open drawer, check product
        close_cart(wait)                                      # Verify 3: close cart drawer

        print("\n" + "=" * 60)
        print("TEST PASSED ✓")
        print("=" * 60 + "\n")
        return True

    except (TimeoutException, NoSuchElementException) as exc:
        print("\n" + "=" * 60)
        print(f"TEST FAILED ✗  —  {exc}")
        print("=" * 60 + "\n")
        return False

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    passed = run_test()
    raise SystemExit(0 if passed else 1)
