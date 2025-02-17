from playwright.sync_api import sync_playwright, Playwright, Page
import re

url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year=2024"

def tournament_details(page: Page, tournament_list:list):
    for i in range(len(tournament_list)):
        url = tournament_list[i]["link"] + "?tab=Resultados"
        page.goto(url)
        
        if "P2" in tournament_list[i]['title']:
            rounds = ['Round of 32', 'Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
        elif "FINALS" in tournament_list[i]['title']:
            rounds = ['Quarterfinals', 'Semifinals', 'Final']
        else:
            rounds = ['Round of 64', 'Round of 32', 'Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
        # rounds_frame = page.locator("div.colDraw.trentaduesimidifinale")
        page.goto(f"https://widget.matchscorerlive.com/screen/resultsbyday/FIP-2024-901/1?t=tol")
        page.wait_for_selector("a.text-decoration-none")
        days = page.locator("a.text-decoration-none")
        for i in range(days.count()):
            day = i+1
            page.goto(f"https://widget.matchscorerlive.com/screen/resultsbyday/FIP-2024-901/{day}?t=tol")
            page.wait_for_selector("div#container")
            match_div = page.locator("div.col-12.p-0")
            
            for j in range(match_div.count()):
                partido = match_div.nth(j)
                score_box = partido.locator("tr.scorebox-header-completed")
                round_name_div = score_box.locator("div.round-name.text-right")
                text_content = round_name_div.text_content()
                patron = r"^\s*(\S.*\S)\s*$"
                gender, round_name = re.findall(patron, text_content, re.MULTILINE)
                
                print(round_name, gender)
                if round_name in rounds and gender == "Men":
                    patron_nombres = r"^[A-Z]\. [A-Za-z]+(?: \(\d+\))?"
                    patron_puntajes = r"^\s*(\d+)\s+(\d+)\s+(\d+|-)"
                    
                    tr_attr = partido.locator("tr")
                    print("--------------")
                    team_1 = tr_attr.nth(1).inner_text()
                    team_2 = tr_attr.nth(2).inner_text()
                    team_1_names = re.findall(patron_nombres, team_1, re.MULTILINE)
                    team_1_scores = re.findall(patron_puntajes, team_1, re.MULTILINE)
                    
                    team_2_names = re.findall(patron_nombres, team_2, re.MULTILINE)
                    team_2_scores = re.findall(patron_puntajes, team_2, re.MULTILINE)
                    print(team_1_names, ": ", team_1_scores)
                    print(team_2_names, ": ", team_2_scores)
                    print("--------------")
            
            # print(tournament_rounds.count
            # rounds = [tournament_rounds.nth(i).inner_text() for i in range(tournament_rounds.count())]
            # print(rounds)
        


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
    tournament_details(page, dict_events)
        # link = event_content.locator("div.event-title").locator("a").get_attribute("href")
        # print(link)


def run(playwright: Playwright, url: str):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    # page.goto("http://example.com")
    scrapp_padel_data(page, url)
    browser.close()

with sync_playwright() as playwright:
    run(playwright, url)