from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.search_locators import SearchLocators

class SearchPage(BasePage):
    def navigate_to_products(self):
        """Điều hướng sang trang Products và chờ ô tìm kiếm xuất hiện"""
        self.click(SearchLocators.PRODUCTS_LINK)
        expect(self.page.locator(SearchLocators.SEARCH_INPUT)).to_be_visible(timeout=5000)

    def search_for(self, keyword):
        """Thực hiện tìm kiếm với thao tác Clear trước khi Fill"""
        self.page.locator(SearchLocators.SEARCH_INPUT).clear()
        self.fill(SearchLocators.SEARCH_INPUT, keyword)
        self.click(SearchLocators.SEARCH_BUTTON)

    def verify_products_found(self, is_found: bool, expected_header: str, keyword: str):
        """
        Xác minh kết quả hiển thị của sản phẩm dựa trên Expected Header.
        Kiểm tra thêm việc từ khóa có nằm trong tên sản phẩm trả về hay không.
        """
        # 1. Xác minh Header
        header_locator = self.page.locator(f"text={expected_header}")
        expect(header_locator).to_be_visible(timeout=5000)
        
        product_list = self.page.locator(SearchLocators.PRODUCT_NAMES)
        
        if is_found:
            # === KỲ VỌNG TÌM THẤY SẢN PHẨM ===
            try:
                # Chờ hiển thị ít nhất 1 sản phẩm
                expect(product_list.first).to_be_visible(timeout=3000)
            except AssertionError:
                # Ném lỗi với thông báo rõ ràng để test báo Fail đúng lý do
                raise AssertionError(f"Hệ thống không trả về bất kỳ sản phẩm nào cho từ khóa '{keyword}'.")

            count = product_list.count()
            
            # YÊU CẦU: Nếu không phải "All Products" -> Phải kiểm tra tên sản phẩm
            if expected_header != "All Products" and keyword:
                # Để dễ dàng so sánh, ta chuyển từ khóa về chữ thường và cắt khoảng trắng thừa
                # Lý do: Trên giao diện web, khoảng trắng dư thừa thường bị HTML ẩn đi.
                clean_keyword = keyword.strip().lower()
                
                # Biến cờ: Chỉ cần có ít nhất 1 sản phẩm chứa từ khóa là đạt yêu cầu
                keyword_matched = False
                
                # Quét tên của tối đa 5 sản phẩm đầu tiên (để tối ưu tốc độ)
                check_limit = min(5, count)
                for i in range(check_limit):
                    product_name = product_list.nth(i).inner_text().lower()
                    if clean_keyword in product_name:
                        keyword_matched = True
                        break
                        
                if not keyword_matched:
                    raise AssertionError(f"Tìm thấy {count} sản phẩm, nhưng không có sản phẩm nào chứa từ khóa '{clean_keyword}'.")
                    
        else:
            # === KỲ VỌNG KHÔNG TÌM THẤY SẢN PHẨM NÀO ===
            self.page.wait_for_timeout(1000) 
            count = product_list.count()
            if count > 0:
                raise AssertionError(f"Kỳ vọng KHÔNG tìm thấy sản phẩm, nhưng lại hiển thị {count} sản phẩm.")