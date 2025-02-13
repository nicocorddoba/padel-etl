from playwright.sync_api import sync_playwright, Playwright, Page

url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year=2024"

def scrapp_padel_data(page: Page, url: str):
    page.goto(url)
    page.wait_for_selector("section#event-data")
    events_section = page.locator("section#event-data")
    events = events_section.locator("section.month-section")
    dict_events = []
    for i in range(events.count()):
        # print(f"Event {i}")
        event = events.nth(i)
        event_content = event.locator("div.event-content-wrap")
        for i in range(event_content.count()):
            tournament = event_content.nth(i)
            link = tournament.locator("div.event-title").locator("a").get_attribute("href")
            title = tournament.locator("div.event-title").inner_text()
            date = tournament.locator("div.date-start-end").inner_text()
            location = tournament.locator("div.event-location").inner_text()
            tournament_dict = {
                "link": link,
                "title": title,
                "date_start": date.split(' ')[1],
                "date_end": date.split(' ')[-1],
                "location": location}
            dict_events.append(tournament_dict)
                
        # link = event_content.locator("div.event-title").locator("a").get_attribute("href")
        # print(link)


def run(playwright: Playwright, url: str):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    # page.goto("http://example.com")
    scrapp_padel_data(page, url)
    browser.close()

with sync_playwright() as playwright:
    run(playwright, url)