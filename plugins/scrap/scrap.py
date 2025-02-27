from playwright.sync_api import sync_playwright, Playwright, Page
import re
import datetime

# url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year=2024"


def winner_calculation(date,team_1,team_1_scores: tuple, team_2_scores: tuple, dict_flag: dict = None) -> str:
    if dict_flag:
        if dict_flag["flag"] == "WO":
            return dict_flag["team"]
        elif dict_flag["flag"] == "RET" or dict_flag["flag"] == "DSQ":
            return "team_2" if dict_flag["team"] == "team_1" else "team_1"
        
    else:
        sets_1 = 0
        sets_2 = 0
        for i in range(3):
            if team_1_scores[i].isnumeric():
                if team_1_scores[i] > team_2_scores[i]: sets_1+=1
                else: sets_2 +=1

        return "team_1" if sets_1 > sets_2 else "team_2"
    

def tournament_details(page: Page, tournament_dict:dict, gender_arg:str):
    url = tournament_dict['link'] + "?tab=Resultados"
    date_start = datetime.datetime.strptime(tournament_dict["date_start"], "%d/%m/%Y")
    match_list = []     
    
    
    if "P2" in tournament_dict['title']:
        rounds = ['Q1', 'Q2', 'Q3', 'Round of 32', 'Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
        
    elif "FINALS" in tournament_dict['title']:
        rounds = ['Quarterfinals', 'Semifinals', 'Final 3rd place', 'Final']
        
    else:
        rounds = ['Q1', 'Q2', 'Round of 64', 'Round of 32', 'Round of 16', 'Quarterfinals', 'Semifinals', 'Final']
        
    # rounds_frame = page.locator("div.colDraw.trentaduesimidifinale")
    page.goto(url)
    page.wait_for_selector("div#event-tab-content-7")
    frame_locator = page.locator("div#event-tab-content-7")
    iframe = frame_locator.locator("iframe.iframe-score.entered.litespeed-loaded")
    src = iframe.get_attribute("src")
    pattern_days = r"/(\d{1,2})\?t=tol"
    days = "".join(re.findall(pattern_days, src))
    new_link = src[:-len(days + '?t=tol')]
    
    for k in range(int(days)):
        number_page = k+1
        date = date_start + datetime.timedelta(days=k)
        page.goto(new_link + f"{number_page}?t=tol")
        page.wait_for_selector("div#container")
        game_div = page.locator("div.col-12.p-0")
        
        for j in range(game_div.count()):
            game = game_div.nth(j)
            score_box = game.locator("tr.scorebox-header-completed")
            round_name_div = score_box.locator("div.round-name.text-right")
            # Raw gender and round name
            text_content = round_name_div.text_content()
            
            # Extracter re pattern for gender and round names
            pattern_round_name = r"^\s*(\S.*\S)\s*$"
            gender, round_name = re.findall(pattern_round_name, text_content, re.MULTILINE)
            round_id_dict = {"Q1":"Q1", "Q2": "Q2", "Q3": 'Q3', 'Round of 64':64, 'Round of 32':32, 'Round of 16':16, 'Quarterfinals':8, 'Semifinals':4, 'Final 3rd place': 3, 'Final':2}
            
            if round_name in rounds and gender == gender_arg:
                # Extracter re pattern for team names and scores
                pattern_names = r"([A-ZÁÉÍÓÚ]\.\s[A-Za-zÁÉÍÓÚáéíóúü]+(?:\s\(\d+\))?)"
                pattern_flag = r"\b(RET|WO|DSQ)\b"
                pattern_scores = r"(\d+|\-)\s+(\d+|\-)\s+(\d+|\-)"
                
                tr_attr = game.locator("tr")
                team_1 = tr_attr.nth(1).inner_text()
                team_2 = tr_attr.nth(2).inner_text()
                
                # Team 1 and Team 2 procesed names and scores and flag (WO, RET, DSQ Or None)
                try:
                    team_1_names = re.findall(pattern_names, team_1, re.MULTILINE)
                    team_1_flag = re.search(pattern_flag, team_1)
                    team_1_scores = re.findall(pattern_scores, team_1, re.MULTILINE)[0]
                    
                    team_2_names = re.findall(pattern_names, team_2, re.MULTILINE)
                    team_2_flag = re.search(pattern_flag, team_2)
                    team_2_scores = re.findall(pattern_scores, team_2, re.MULTILINE)[0]
                except Exception as e:
                    print(e)
                if team_1_flag:
                    dict_flag = {"team": "team_1","flag":team_1_flag.group(0)}
                elif team_2_flag:
                    dict_flag = {"team": "team_2", "flag": team_2_flag.group(0)}
                else: dict_flag = None
                # Id construction: 
                date_id_format = date.strftime('%d%m%y')
                location = tournament_dict['location'][:2]
                round = round_id_dict[round_name]
                team_1_initials = ''.join([i[:4].replace('. ', '') for i in team_1_names])
                team_2_initials = ''.join([i[:4].replace('. ', '') for i in team_2_names])
                # Match id(day, month, year, torunament category, first letter of location, round, 2 first letter of team 1 and team 2)
                match_id = f"{date_id_format}{location}{round}{team_1_initials}{team_2_initials}"
                match_dict = {"id":match_id,
                                "date": date.strftime('%d/%m/%Y'), 
                                "round_name": round_name,
                                "team_1": team_1_names, 
                                "team_1_scores": team_1_scores, 
                                "team_2": team_2_names, 
                                "team_2_scores": team_2_scores, 
                                "winner": winner_calculation(date,team_1_names,team_1_scores, team_2_scores, dict_flag)}
                match_list.append(match_dict)
                
    return match_list        
        

def scrap_padel_data(page: Page, url: str, gender_arg: str):
    page.goto(url)
    page.wait_for_selector("section#event-data")
    events_section = page.locator("section#event-data")
    events = events_section.locator("div.event-container")
    list_events = []

    for i in range(events.count()):
        # page.goto(url)
        tournament = events.nth(i)
        link = tournament.locator("div.event-title").locator("a").get_attribute("href")
        title = tournament.locator("div.event-title").inner_text()
        date = tournament.locator("div.date-start-end").inner_text()
        location = tournament.locator("div.event-location").inner_text()
        tournament_dict = {
            "link": link,
            "title": title,
            "date_start": date.split(' ')[1],
            "location": location}
        list_events.append(tournament_dict)
    for i in range(len(list_events)):
        # tournament_dict = list_events[i
        tournament_dict = list_events[i]
        match_list = tournament_details(page, tournament_dict, gender_arg)
        tournament_dict["matches"] = match_list

    return list_events

def run(url: str, gender_arg: str):
    with sync_playwright() as playwright:
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=True)
        page = browser.new_page()
        # page.goto("http://example.com")
        list_events = scrap_padel_data(page, url, gender_arg)
        browser.close()
        return list_events
