import pytest
from pages.search_page import SearchPage
from utils.excel_utils import load_excel_data
from config.config import DATA_FILE

search_cases = load_excel_data(DATA_FILE, "SearchData")

@pytest.mark.parametrize("case", search_cases)
def test_search(driver_setup, request, case):
    request.node.test_id = case.get("TestCaseID", "SearchTest")
    page = driver_setup["page"]
    search_page = SearchPage(page)
    
    search_text = str(case.get("SearchText", ""))
    search_page.search_for(search_text)

    if str(case.get("ProductFound")).upper() == "Y":
        contain_text = search_text if str(case.get("ContainText")).upper() == "Y" else ""
        search_page.verify_products_displayed(contain_text)