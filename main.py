from playwright.sync_api import sync_playwright, Playwright, Page

url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year=2024"

def scrapp_padel_data(page: Page, url: str):
    page.goto(url)
    page.wait_for_selector("section#event-data")
    events_section = page.locator("section#event-data")
    events = events_section.locator("section.month-section")
    
    for i in range(events.count()):
        # print(f"Event {i}")
        event = events.nth(i)
        print(event.get_attribute("id"))


def run(playwright: Playwright, url: str):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    # page.goto("http://example.com")
    scrapp_padel_data(page, url)
    browser.close()

with sync_playwright() as playwright:
    run(playwright, url)