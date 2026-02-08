from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

class DashboardPage:

    # Sort dropdown button
    SORT_DROPDOWN = (By.XPATH, "//button[@role='combobox']")
    SORT_DROPDOWN_ALT = (By.XPATH, "//button[contains(normalize-space(),'Select')]")
    SORT_OPTIONS = (By.XPATH, "//*[@role='option']")
    
    # Product buttons and elements
    SAMPLE_SHIRT_ADD_TO_CART = (By.XPATH, "//div[8]//div[1]//button[1]")
    SAMPLE_SHOE_IMAGE = (By.XPATH, "//img[@alt='Sample Shoe Name']")
    INCREASE_QUANTITY_BTN = (By.XPATH, "//button[normalize-space()='+']")
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(text(),'Add to cart')]")
    BACK_TO_PRODUCTS_BTN = (By.XPATH, "//button[@class='flex items-center gap-2 text-black font-semibold mb-8 cursor-pointer']")
    SAMPLE_SUNGLASS_FAVORITE = (By.XPATH, "//div[@class='products grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6']//div[2]//span[1]//button[1]")
    SAMPLE_SHIRT_REMOVE = (By.XPATH, "//div[8]//div[1]//button[normalize-space()='Remove from cart']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def scroll_to_element(self, element):
        """Scroll element into view"""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)

    def click_element(self, locator, element_name="element"):
        """Smart click with fallback to JavaScript"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.scroll_to_element(element)
            
            # Wait for element to be clickable
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            print(f" Clicked {element_name} (normal click)")
        except (TimeoutException, ElementClickInterceptedException) as e:
            print(f" Normal click failed, using JavaScript click...")
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)
            print(f" Clicked {element_name} (JavaScript click)")

    def find_dropdown_button(self):
        """Try to find the dropdown button with multiple strategies"""
        try:
            elem = self.driver.find_element(*self.SORT_DROPDOWN)
            if elem.is_displayed():
                return elem
        except:
            pass
        
        try:
            elem = self.driver.find_element(*self.SORT_DROPDOWN_ALT)
            if elem.is_displayed():
                return elem
        except:
            pass
        
        return None

    def wait_for_page_ready(self, max_wait=15):
        """Wait for the page to be fully loaded"""
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            try:
                ready = self.driver.execute_script("return document.readyState")
                
                if ready == "complete":
                    time.sleep(0.5)
                    dropdown = self.find_dropdown_button()
                    if dropdown:
                        return True
                
                time.sleep(1)
            except:
                time.sleep(1)
        
        return False

    def select_sort_option(self, option_text):
        """Select a sort option by partial text match"""
        print(f"\n{'='*70}")
        print(f"SELECTING: '{option_text}'")
        print('='*70)
        
        self.wait_for_page_ready(max_wait=20)
        
        dropdown = self.find_dropdown_button()
        if not dropdown:
            raise Exception("Dropdown button not found")
        
        dropdown.click()
        time.sleep(1)
        
        options = self.wait.until(
            EC.presence_of_all_elements_located(self.SORT_OPTIONS)
        )
        
        option_clicked = False
        for idx, option in enumerate(options):
            option_full_text = option.text.strip()
            if option_full_text and option_text.lower() in option_full_text.lower():
                try:
                    option.click()
                except:
                    self.driver.execute_script("arguments[0].click();", option)
                
                option_clicked = True
                break
        
        if not option_clicked:
            available = [opt.text.strip() for opt in options]
            raise Exception(f"Option '{option_text}' not found. Available: {available}")
        
        time.sleep(3)

    def get_all_sort_options(self):
        """Get all available sort options"""
        dropdown = self.find_dropdown_button()
        if not dropdown:
            raise Exception("Dropdown button not found")
        
        dropdown.click()
        time.sleep(0.5)
        options = self.wait.until(
            EC.presence_of_all_elements_located(self.SORT_OPTIONS)
        )
        
        option_texts = [opt.text.strip() for opt in options if opt.text.strip()]
        
        try:
            dropdown.click()
            time.sleep(0.3)
        except:
            pass
        
        return option_texts

    def verify_sort_order_in_url(self, expected_param):
        """Verify the URL contains the expected order_by parameter"""
        current_url = self.driver.current_url
        is_valid = expected_param in current_url
        return is_valid

    # Cart and product interaction methods
    
    def click_add_to_cart_sample_shirt(self):
        """Click 'Add to cart' button for Sample Shirt"""
        print("\n Adding Sample Shirt to cart...")
        self.click_element(self.SAMPLE_SHIRT_ADD_TO_CART, "Sample Shirt Add to Cart button")
        time.sleep(1)
        print("  Sample Shirt added to cart")

    def click_sample_shoe_image(self):
        """Click on Sample Shoe image to view details"""
        print("\n Clicking Sample Shoe image...")
        self.click_element(self.SAMPLE_SHOE_IMAGE, "Sample Shoe image")
        time.sleep(1)
        print("  Sample Shoe details page opened")

    def increase_quantity_to(self, quantity):
        """Increase quantity by clicking + button"""
        print(f"\n Increasing quantity to {quantity}...")
        
        # Click the + button (quantity - 1) times (default is 1)
        for i in range(quantity - 1):
            self.click_element(self.INCREASE_QUANTITY_BTN, "+ button")
            time.sleep(0.5)
            print(f"  Quantity now: {i + 2}")
        
        print(f"  Quantity set to {quantity}")

    def click_add_to_cart_on_details_page(self):
        """Click 'Add to cart' button on product details page"""
        print("\n Adding product to cart from details page...")
        self.click_element(self.ADD_TO_CART_BTN, "Add to Cart button")
        time.sleep(1)
        print("  Product added to cart")

    def click_back_to_products(self):
        """Click 'Back to products' button"""
        print("\n Going back to products page...")
        self.click_element(self.BACK_TO_PRODUCTS_BTN, "Back to Products button")
        time.sleep(2)
        print("   Returned to products page")

    def remove_sample_shirt_from_cart(self):
        """Remove Sample Shirt from cart on dashboard page"""
        print("\n Removing Sample Shirt from cart...")
        self.click_element(self.SAMPLE_SHIRT_REMOVE, "Sample Shirt Remove from Cart button")
        time.sleep(1)
        print("  Sample Shirt removed from cart")

    def add_favorite_sample_sunglass(self):
        """Add Sample Sunglass to favorites"""
        print("\n Adding Sample Sunglass to favorites...")
        
        try:
            # Find the button element (not SVG)
            element = self.wait.until(
                EC.presence_of_element_located(self.SAMPLE_SUNGLASS_FAVORITE)
            )
            
            # Scroll to it
            self.scroll_to_element(element)
            
            # Wait for it to be clickable
            element = self.wait.until(
                EC.element_to_be_clickable(self.SAMPLE_SUNGLASS_FAVORITE)
            )
            
            # Try normal click first
            try:
                element.click()
                print("   Sample Sunglass added to favorites (normal click)")
            except:
                # Fallback to JavaScript click on the button element
                self.driver.execute_script("arguments[0].click();", element)
                print("   Sample Sunglass added to favorites (JavaScript click)")
            
            time.sleep(1)
        except Exception as e:
            print(f"  Error adding to favorites: {str(e)[:100]}")
            raise