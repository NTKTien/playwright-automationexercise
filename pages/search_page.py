from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.search_locators import SearchLocators

class SearchPage(BasePage):
    def search_for(self, keyword):
        self.click(SearchLocators.PRODUCTS_LINK)
        self.fill(SearchLocators.SEARCH_INPUT, keyword)
        self.click(SearchLocators.SEARCH_BUTTON)

    def verify_products_displayed(self, expected_keyword):
        expect(self.page.locator(SearchLocators.SEARCHED_PRODUCTS_TITLE)).to_be_visible()
        product_list = self.page.locator(SearchLocators.PRODUCT_NAMES)
        count = product_list.count()
        assert count > 0, "Không có sản phẩm nào được hiển thị"
        
        if expected_keyword and expected_keyword.lower() != 'none':
            for i in range(count):
                text = product_list.nth(i).inner_text()
                assert expected_keyword.lower() in text.lower(), f"Sản phẩm {text} không chứa từ khóa {expected_keyword}"