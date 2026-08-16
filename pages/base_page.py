from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str):
        base = self.page.url.split('/#')[0].split('.com')[0] + '.com'
        self.page.goto(f"{base}{path}", wait_until="domcontentloaded")

    def click(self, selector: str):
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        # If text is None, set it to an empty string to clear the input.
        # If it's the number 0 (int), keep it as "0".
        val = "" if text is None else str(text)
        self.page.fill(selector, val)