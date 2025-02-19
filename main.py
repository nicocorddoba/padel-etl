from playwright.sync_api import sync_playwright, Playwright, Page
import re
import datetime

url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year=2024"


def winner_calculation(team_1_scores: tuple, team_2_scores: tuple) -> str:
    t1_total_score = sum(
        [int(i[0]) for i in team_1_scores if i != "-"])
    t2_total_score = sum(
        [int(i[0]) for i in team_2_scores if i != "-"])
    return "team_1" if t1_total_score > t2_total_score else "team_2"
    

def tournament_details(page: Page, tournament_list:list):
    for i in range(len(tournament_list)):
        url = tournament_list[i]["link"] + "?tab=Resultados"
        
        date_start = datetime.datetime.strptime(tournament_list[i]["date_start"], "%d/%m/%Y")
        
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
        
        for k in range(days.count()):
            day = k+1
            date = date_start + datetime.timedelta(days=day)
            page.goto(f"https://widget.matchscorerlive.com/screen/resultsbyday/FIP-2024-901/{day}?t=tol")
            page.wait_for_selector("div#container")
            match_div = page.locator("div.col-12.p-0")
            
            for j in range(match_div.count()):
                partido = match_div.nth(j)
                score_box = partido.locator("tr.scorebox-header-completed")
                round_name_div = score_box.locator("div.round-name.text-right")
                text_content = round_name_div.text_content()
                pattern_round_name = r"^\s*(\S.*\S)\s*$"
                gender, round_name = re.findall(pattern_round_name, text_content, re.MULTILINE)
                round_id_dict = {'Round of 64':64, 'Round of 32':32, 'Round of 16':16, 'Quarterfinals':8, 'Semifinals':4, 'Final':2}
                match_list = []
                print(round_name, gender)       
                if round_name in rounds and gender == "Men":
                    pattern_nombres = r"^[A-Z]\. [A-Za-z]+(?: \(\d+\))?"
                    pattern_puntajes = r"^\s*(\d+)\s+(\d+)\s+(\d+|-)"
                    
                    tr_attr = partido.locator("tr")
                    print("--------------")
                    team_1 = tr_attr.nth(1).inner_text()
                    team_2 = tr_attr.nth(2).inner_text()
                    team_1_names = re.findall(pattern_nombres, team_1, re.MULTILINE)
                    team_1_scores = re.findall(pattern_puntajes, team_1, re.MULTILINE)[0]
                    
                    team_2_names = re.findall(pattern_nombres, team_2, re.MULTILINE)
                    team_2_scores = re.findall(pattern_puntajes, team_2, re.MULTILINE)[0]
                    print(team_1_names, team_1_scores)
                    
                    # Match id(day, month, year, torunament category, first letter of location, round, 2 first letter of team 1 and team 2)
                    match_id = f"{date.strftime('%d/%m/%Y')}{tournament_list[i]['location'][0]}{round_id_dict[round_name]}{''.join([i[:3].replace('. ', '') for i in team_1_names])}{''.join([i[:3].replace('. ', '') for i in team_2_names])}"
                                
                    match_dict = {"id":match_id,"date": date, "team_1": team_1_names, "team_1_scores": team_1_scores, "team_2": team_2_names, "team_2_scores": team_2_scores, "winner": winner_calculation(team_1_scores, team_2_scores)}
                    print(match_dict)
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