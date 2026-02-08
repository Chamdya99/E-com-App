import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.cart_page import CartPage
from config.config import Config

@pytest.mark.cart
def test_checkout_process(setup):
    """Test complete checkout process from cart to order completion"""
    driver = setup
    config = Config()

    login_page = LoginPage(driver)
    dashboard = DashboardPage(driver)
    cart_page = CartPage(driver)

    # Login
    print("\n" + "="*70)
    print("LOGGING IN")
    print("="*70)
    login_page.login(config.EMAIL, config.PASSWORD)
    time.sleep(2)

    # Step 1: Add Sample Shirt to cart
    print("\n" + "="*70)
    print("STEP 1: ADD SAMPLE SHIRT TO CART")
    print("="*70)
    dashboard.click_add_to_cart_sample_shirt()
    print("Sample Shirt added to cart")

    # Step 2: Click cart icon and go to cart page
    print("\n" + "="*70)
    print("STEP 2: NAVIGATE TO CART PAGE")
    print("="*70)
    cart_page.click_cart_icon()
    print("Cart page opened")

    # Step 3: Click Checkout
    print("\n" + "="*70)
    print("STEP 3: CLICK CHECKOUT")
    print("="*70)
    cart_page.click_checkout()
    print("✓ Checkout initiated")

    # Step 4: Fill checkout form (3 fields only)
    print("\n" + "="*70)
    print("STEP 4: FILL CHECKOUT FORM")
    print("="*70)
    cart_page.fill_checkout_form(
        first_name="John",
        last_name="Doe",
        postcode="123"
    )
    print("Form filled successfully")

    # Step 5: Click Continue
    print("\n" + "="*70)
    print("STEP 5: CLICK CONTINUE")
    print("="*70)
    cart_page.click_continue()
    print("Continued to next step")

    # Step 6: Click Finish
    print("\n" + "="*70)
    print("STEP 6: CLICK FINISH")
    print("="*70)
    cart_page.click_finish()
    print(" Order completed")

    # Step 7: Click Continue Shopping
    print("\n" + "="*70)
    print("STEP 7: CLICK CONTINUE SHOPPING")
    print("="*70)
    cart_page.click_continue_shopping()
    print("Continue shopping clicked")

    # Step 8: Verify back to home page
    print("\n" + "="*70)
    print("STEP 8: VERIFY BACK TO HOME PAGE")
    print("="*70)
    cart_page.verify_back_to_home_page()
    print("Verified back on home page")
    
@pytest.mark.cart
def test_logout_only(setup):
    """Test logout functionality only"""
    driver = setup
    config = Config()

    login_page = LoginPage(driver)
    cart_page = CartPage(driver)

    # Login
    print("\n" + "="*70)
    print("LOGGING IN")
    print("="*70)
    login_page.login(config.EMAIL, config.PASSWORD)
    time.sleep(2)
    print("Login successful")

    # Logout
    print("\n" + "="*70)
    print("LOGOUT")
    print("="*70)
    cart_page.click_logout()
    print(" Logout clicked")

    # Verify logout
    print("\n" + "="*70)
    print("VERIFY LOGOUT")
    print("="*70)
    cart_page.verify_logout_successful()
    print("Logout verified successfully")

    print("\n" + "="*70)
    print("LOGOUT TEST PASSED ")
    print("="*70)