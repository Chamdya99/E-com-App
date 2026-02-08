import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config

@pytest.mark.dashboard
def test_sort_dropdown_options(setup):
    driver = setup
    config = Config()

    login_page = LoginPage(driver)
    dashboard = DashboardPage(driver)

    # Login
    print("\n" + "="*70)
    print("LOGGING IN")
    print("="*70)
    login_page.login(config.EMAIL, config.PASSWORD)
    time.sleep(2)

    # Get all available options
    print("\n" + "="*70)
    print("STEP 1: GET ALL DROPDOWN OPTIONS")
    print("="*70)
    options = dashboard.get_all_sort_options()
    print("\nAvailable options:")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")

    # Validate options
    assert len(options) == 4, f"Expected 4 options, found {len(options)}"
    print("✓ All expected options found")

    # Test sorting options
    print("\n" + "="*70)
    print("STEP 2: SELECT 'A TO Z (ASCENDING)'")
    print("="*70)
    dashboard.select_sort_option("A to Z")
    assert dashboard.verify_sort_order_in_url("order_by=asc")
    print("✓ Ascending sort applied")

    print("\n" + "="*70)
    print("STEP 3: SELECT 'Z TO A (DESCENDING)'")
    print("="*70)
    dashboard.select_sort_option("Z to A")
    assert dashboard.verify_sort_order_in_url("order_by=dsc")
    print("✓ Descending sort applied")

    print("\n" + "="*70)
    print("STEP 4: SELECT 'LOW TO HIGH (PRICE)'")
    print("="*70)
    dashboard.select_sort_option("Low to High")
    assert dashboard.verify_sort_order_in_url("order_by=low")
    print("✓ Price ascending sort applied")

    print("\n" + "="*70)
    print("STEP 5: SELECT 'HIGH TO LOW (PRICE)'")
    print("="*70)
    dashboard.select_sort_option("High to Low")
    assert dashboard.verify_sort_order_in_url("order_by=high")
    print("✓ Price descending sort applied")

    print("\n" + "="*70)
    print("✓✓✓ ALL SORTING TESTS PASSED ✓✓✓")
    print("="*70)


@pytest.mark.dashboard
def test_product_cart_interactions(setup):
    """Test adding products to cart, modifying quantity, and favorites"""
    driver = setup
    config = Config()

    login_page = LoginPage(driver)
    dashboard = DashboardPage(driver)

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

    # Step 2: Click Sample Shoe image
    print("\n" + "="*70)
    print("STEP 2: OPEN SAMPLE SHOE DETAILS")
    print("="*70)
    dashboard.click_sample_shoe_image()
    print("Sample Shoe details opened")

    # Step 3: Increase quantity to 2
    print("\n" + "="*70)
    print("STEP 3: INCREASE QUANTITY TO 2")
    print("="*70)
    dashboard.increase_quantity_to(2)
    print("Quantity increased to 2")

    # Step 4: Add to cart
    print("\n" + "="*70)
    print("STEP 4: ADD SAMPLE SHOE TO CART")
    print("="*70)
    dashboard.click_add_to_cart_on_details_page()
    print("Sample Shoe (qty: 2) added to cart")

    # Step 5: Go back to products page
    print("\n" + "="*70)
    print("STEP 5: BACK TO PRODUCTS PAGE")
    print("="*70)
    dashboard.click_back_to_products()
    print(" Returned to products page")

    # Step 6: Remove Sample Shirt from cart (on dashboard)
    print("\n" + "="*70)
    print("STEP 6: REMOVE SAMPLE SHIRT FROM CART")
    print("="*70)
    dashboard.remove_sample_shirt_from_cart()
    print(" Sample Shirt removed from cart")

    # Step 7: Add Sample Sunglass to favorites
    print("\n" + "="*70)
    print("STEP 7: ADD SAMPLE SUNGLASS TO FAVORITES")
    print("="*70)
    dashboard.add_favorite_sample_sunglass()
    print("Sample Sunglass added to favorites")

    print("\n" + "="*70)
    print(" ALL PRODUCT/CART TESTS PASSED ")
    print("="*70)