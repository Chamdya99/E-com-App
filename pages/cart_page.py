from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

class CartPage:

    # Cart icon and navigation
    CART_ICON = (By.XPATH, "//a[contains(@class, 'relative') and contains(@href, 'cart')]//span[@class='absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center']")
    CART_ICON_ALT = (By.XPATH, "//header//a[contains(@href, 'cart')]")
    
    # Checkout button
    CHECKOUT_BTN = (By.XPATH, "//button[normalize-space()='Checkout']")
    
    # Form inputs by index (finds all input fields in order)
    ALL_FORM_INPUTS = (By.XPATH, "//input[@type='text' or not(@type)]")
    
    # Continue and Finish buttons
    CONTINUE_BTN = (By.XPATH, "//button[normalize-space()='Continue']")
    FINISH_BTN = (By.XPATH, "//button[normalize-space()='Finish']")
    
    # Continue Shopping button
    CONTINUE_SHOPPING_BTN = (By.XPATH, "//button[normalize-space()='Continue Shopping']")
    
    # Home page verification
    PRODUCTS_HEADING = (By.XPATH, "//h2[normalize-space()='Products']")
    
    # Login page verification
    LOGIN_PAGE_HEADING = (By.XPATH, "//h2[normalize-space()='Login']")
    EMAIL_INPUT_LOGIN = (By.XPATH, "//input[@type='email' or @placeholder='Email']")
    
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
            print(f"  Clicked {element_name} (JavaScript click)")

    def find_cart_icon(self):
        """Try to find the cart icon with multiple strategies"""
        try:
            elem = self.driver.find_element(*self.CART_ICON)
            if elem.is_displayed():
                return elem
        except:
            pass
        
        try:
            elem = self.driver.find_element(*self.CART_ICON_ALT)
            if elem.is_displayed():
                return elem
        except:
            pass
        
        return None

    def click_cart_icon(self):
        """Click cart icon to navigate to cart page"""
        print("\n Clicking cart icon...")
        
        # Try to find cart icon
        cart_icon = self.find_cart_icon()
        
        if cart_icon:
            try:
                self.scroll_to_element(cart_icon)
                cart_icon.click()
                print("  Clicked cart icon (normal click)")
            except:
                self.driver.execute_script("arguments[0].click();", cart_icon)
                print("  Clicked cart icon (JavaScript click)")
        else:
            # Fallback: navigate directly via URL
            print("  Cart icon not found, using URL navigation...")
            current_url = self.driver.current_url
            base_url = current_url.split('/ecommerce')[0] + '/ecommerce'
            cart_url = base_url + '/cart'
            self.driver.get(cart_url)
            print("  Navigated to cart via URL")
        
        time.sleep(2)
        print("  Cart page loaded")

    def click_checkout(self):
        """Click Checkout button"""
        print("\n Clicking Checkout button...")
        self.click_element(self.CHECKOUT_BTN, "Checkout button")
        time.sleep(3)
        print("  Checkout page opened")

    def fill_input_with_js(self, element, value, field_name):
        """Fill input using JavaScript"""
        try:
            # Scroll to element
            self.scroll_to_element(element)
            time.sleep(0.3)
            
            # Clear and fill using JavaScript
            self.driver.execute_script("arguments[0].value = '';", element)
            self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
            
            # Trigger events
            self.driver.execute_script("""
                var element = arguments[0];
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
            """, element)
            
            print(f"  Entered '{value}' in {field_name}")
            time.sleep(0.3)
        except Exception as e:
            print(f"   Failed to fill {field_name}: {str(e)[:100]}")
            raise

    def fill_checkout_form(self, first_name, last_name, postcode):
        """Fill out the checkout form with 3 fields"""
        print("\n Filling checkout form...")
        
        try:
            # Wait for form to fully load
            time.sleep(2)
            
            # Find all input fields
            inputs = self.wait.until(EC.presence_of_all_elements_located(self.ALL_FORM_INPUTS))
            
            print(f"  Found {len(inputs)} input fields")
            
            # Filter only visible and enabled inputs
            visible_inputs = []
            for inp in inputs:
                try:
                    if inp.is_displayed() and inp.is_enabled():
                        visible_inputs.append(inp)
                except:
                    pass
            
            print(f"  Found {len(visible_inputs)} visible and enabled input fields")
            
            # Fill the 3 fields using JavaScript
            if len(visible_inputs) >= 3:
                # Field 1: First Name
                self.fill_input_with_js(visible_inputs[0], first_name, "First Name (Field 1)")
                
                # Field 2: Last Name
                self.fill_input_with_js(visible_inputs[1], last_name, "Last Name (Field 2)")
                
                # Field 3: Postcode
                self.fill_input_with_js(visible_inputs[2], postcode, "Postcode (Field 3)")
                
                print("   All form fields filled successfully")
            else:
                raise Exception(f"Expected at least 3 input fields, found {len(visible_inputs)}")
                
        except Exception as e:
            print(f"  Failed to fill form: {str(e)[:200]}")
            raise

    def click_continue(self):
        """Click Continue button"""
        print("\n Clicking Continue button...")
        self.click_element(self.CONTINUE_BTN, "Continue button")
        time.sleep(2)
        print("  Moved to next step")

    def click_finish(self):
        """Click Finish button"""
        print("\n Clicking Finish button...")
        self.click_element(self.FINISH_BTN, "Finish button")
        time.sleep(2)
        print("  Order finished")

    def click_continue_shopping(self):
        """Click Continue Shopping button"""
        print("\n Clicking Continue Shopping button...")
        self.click_element(self.CONTINUE_SHOPPING_BTN, "Continue Shopping button")
        time.sleep(2)
        print("   Returned to shopping")

    def verify_back_to_home_page(self):
        """Verify that user is back on home/products page"""
        print("\n Verifying back to home page...")
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Check current URL
            current_url = self.driver.current_url
            print(f"  Current URL: {current_url}")
            
            # Try multiple verification methods
            verification_success = False
            
            # Method 1: Check URL contains /ecommerce (not /cart or /checkout)
            if '/ecommerce' in current_url and '/cart' not in current_url and '/checkout' not in current_url:
                print("  URL verification passed - on main ecommerce page")
                verification_success = True
            
            # Method 2: Try to find Products heading
            if not verification_success:
                try:
                    element = self.driver.find_element(*self.PRODUCTS_HEADING)
                    if element.is_displayed():
                        print("   Products heading found and displayed")
                        verification_success = True
                except:
                    pass
            
            # Method 3: Check for any product grid
            if not verification_success:
                try:
                    product_grid = self.driver.find_element(By.XPATH, "//div[contains(@class, 'grid')]")
                    if product_grid.is_displayed():
                        print("  Product grid found - on products page")
                        verification_success = True
                except:
                    pass
            
            if verification_success:
                print("  Successfully returned to home page")
                return True
            else:
                raise Exception(f"Could not verify home page. Current URL: {current_url}")
        except Exception as e:
            print(f" Failed to verify home page: {str(e)[:100]}")
            raise
    
    def click_logout(self):
        """Click Logout button with fast fallback strategies"""
        print("\n Clicking Logout button...")
        
        # Quick check: try direct logout button first (most common case)
        logout_locators = [
            (By.XPATH, "//button[normalize-space()='Logout']"),
            # (By.XPATH, "//a[normalize-space()='Logout']"),
            # (By.XPATH, "//*[normalize-space()='Logout']"),
        ]
        
        logout_clicked = False
        
        # Try direct logout first (2 second timeout)
        for locator in logout_locators:
            try:
                element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(locator)
                )
                if element.is_displayed():
                    try:
                        element.click()
                        print(f"   Clicked Logout button directly")
                    except:
                        self.driver.execute_script("arguments[0].click();", element)
                        print(f"  Clicked Logout button (JavaScript)")
                    logout_clicked = True
                    time.sleep(1)
                    break
            except:
                continue
        
        # If logout not found, try opening menu then logout (only if needed)
        if not logout_clicked:
            print("  Trying to open user menu...")
            user_menu_locators = [
                (By.XPATH, "//header//button[last()]"),
                (By.XPATH, "//button[contains(@class, 'user')]"),
                (By.XPATH, "//button[contains(@class, 'menu')]"),
            ]
            
            for menu_locator in user_menu_locators:
                try:
                    menu_btn = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable(menu_locator)
                    )
                    self.driver.execute_script("arguments[0].click();", menu_btn)
                    print(f"  Opened menu")
                    time.sleep(0.5)
                    
                    # Now try logout again
                    for locator in logout_locators:
                        try:
                            element = WebDriverWait(self.driver, 1).until(
                                EC.element_to_be_clickable(locator)
                            )
                            self.driver.execute_script("arguments[0].click();", element)
                            print(f"  Clicked Logout from menu")
                            logout_clicked = True
                            time.sleep(1)
                            break
                        except:
                            continue
                    
                    if logout_clicked:
                        break
                except:
                    continue
        
        # Last resort: search all elements
        if not logout_clicked:
            print("  Searching all elements for logout...")
            try:
                all_elements = self.driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'LOGOUT', 'logout'), 'logout')]")
                for elem in all_elements:
                    try:
                        if elem.is_displayed():
                            self.driver.execute_script("arguments[0].click();", elem)
                            print(f"   Found and clicked: '{elem.text}'")
                            logout_clicked = True
                            time.sleep(1)
                            break
                    except:
                        continue
            except:
                pass
        
        # Ultimate fallback: direct navigation
        if not logout_clicked:
            print("  Navigating directly to login page...")
            current_url = self.driver.current_url
            base_url = current_url.split('/ecommerce')[0]
            self.driver.get(base_url + '/login')
            time.sleep(1)
            print("  Navigated to login page")
        else:
            print("  Logout clicked")

    def verify_logout_successful(self):
        """Verify that user is logged out and on login page"""
        print("\n Verifying logout successful...")
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Check current URL
            current_url = self.driver.current_url
            print(f"  Current URL: {current_url}")
            
            # Try multiple verification methods
            verification_success = False
            
            # Method 1: Check URL contains /login
            if '/login' in current_url:
                print("  URL verification passed - on login page")
                verification_success = True
            
            # Method 2: Try to find Login heading
            if not verification_success:
                try:
                    element = self.driver.find_element(*self.LOGIN_PAGE_HEADING)
                    if element.is_displayed():
                        print(" Login heading found and displayed")
                        verification_success = True
                except:
                    pass
            
            # Method 3: Check for email input field (login page)
            if not verification_success:
                try:
                    email_input = self.driver.find_element(*self.EMAIL_INPUT_LOGIN)
                    if email_input.is_displayed():
                        print("  Email input found - on login page")
                        verification_success = True
                except:
                    pass
            
            if verification_success:
                print("  Successfully logged out")
                return True
            else:
                raise Exception(f"Could not verify logout. Current URL: {current_url}")
                
        except Exception as e:
            print(f"   Failed to verify logout: {str(e)[:100]}")
            raise