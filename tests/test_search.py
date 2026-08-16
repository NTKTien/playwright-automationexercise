import pytest
from playwright.sync_api import expect
from pages.search_page import SearchPage
from utils.excel_utils import load_excel_data
from config.config import DATA_FILE
from utils.logger import get_logger

logger = get_logger(__name__)
search_cases = load_excel_data(DATA_FILE, "SearchData")

@pytest.mark.parametrize("case", search_cases)
def test_search_flow(driver_setup, request, case):
    request.node.test_id = case.get("TestCaseID", "SearchTest")
    logger.info(f"--- Bắt đầu test: {request.node.test_id} ---")
    
    page = driver_setup["page"]
    search_page = SearchPage(page)
    
    # Get test data from the Excel file
    search_keyword = case.get("SearchKeyword")
    expected_header = str(case.get("Expected Header", "Searched Products")).strip()
    product_found = str(case.get("ProductFound", "N")).strip().upper()
    is_found_expected = (product_found == "Y")
    
    # Execute the search
    search_page.navigate("/")
    search_page.navigate_to_products()
    search_page.search_for(search_keyword)
    
    # Verify the results
    try:
        # Pass the search keyword to match product names
        search_page.verify_products_found(is_found_expected, expected_header, str(search_keyword or ""))
        logger.info(f"Test Pass: Displaying '{expected_header}' and correct results (ProductFound={product_found}).")
    except AssertionError as e:
        pytest.fail(f"Error verifying results: {str(e)}")