from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.search_locators import SearchLocators
from config.config import TIMEOUT_STANDARD, WAIT_NO_RESULT

class SearchPage(BasePage):
    def navigate_to_products(self):
        """Navigate to the Products page and wait for the search input to appear"""
        self.click(SearchLocators.PRODUCTS_LINK)
        expect(self.page.locator(SearchLocators.SEARCH_INPUT)).to_be_visible(timeout=TIMEOUT_STANDARD)

    def search_for(self, keyword):
        """Perform a search with a clear operation before filling"""
        self.page.locator(SearchLocators.SEARCH_INPUT).clear()
        self.fill(SearchLocators.SEARCH_INPUT, keyword)
        self.click(SearchLocators.SEARCH_BUTTON)

    def verify_products_found(self, is_found: bool, expected_header: str, keyword: str):
        """
        Verify the search results based on the expected header.
        Check additionally if the keyword is present in the returned product names.
        """
        # 1. Verify Header
        header_locator = self.page.locator(f"text={expected_header}")
        expect(header_locator).to_be_visible(timeout=TIMEOUT_STANDARD)
        
        product_list = self.page.locator(SearchLocators.PRODUCT_NAMES)
        
        if is_found:
            # === EXPECTED: FOUND PRODUCTS ===
            try:
                # Wait for at least 1 product to be visible
                expect(product_list.first).to_be_visible(timeout=TIMEOUT_STANDARD)
            except AssertionError:
                # Throw an error with a clear message for the test to report Fail correctly
                raise AssertionError(f"System did not return any products for the keyword '{keyword}'.")

            count = product_list.count()
            
            # EXPECTED: If it's not "All Products" -> Must check product names
            if expected_header != "All Products" and keyword:
                # To make comparison easier, convert the keyword to lowercase and trim whitespace
                # Reason: On the web interface, extra whitespace is often hidden by HTML.
                clean_keyword = keyword.strip().lower()
                
                # Flag: Just need at least 1 product containing the keyword to meet the requirement
                keyword_matched = False
                
                # Scan the names of up to 5 products (for performance optimization)
                check_limit = min(5, count)
                for i in range(check_limit):
                    product_name = product_list.nth(i).inner_text().lower()
                    if clean_keyword in product_name:
                        keyword_matched = True
                        break
                        
                if not keyword_matched:
                    raise AssertionError(f"Found {count} products, but none contain the keyword '{clean_keyword}'.")
                    
        else:
            # === EXPECTED: NOT FOUND ANY PRODUCTS ===
            self.page.wait_for_timeout(WAIT_NO_RESULT)
            count = product_list.count()
            if count > 0:
                raise AssertionError(f"Expected NO products, but {count} products were displayed.")