import pandas as pd
import json
import re

def extract_data(path: str) -> list[dict]:
    try: 
        with open (path, encoding='utf-8') as f:
            raw_data = json.load(f)
            f.close()

        matches = []
        tournaments = []
        for event in raw_data:
            for match in event["matches"]:
                match['event_title'] = event['title']
                matches.append(match)
            event.pop('matches')
            tournaments.append(event)
        return matches, tournaments
    except Exception as e:
        print(e)
        

def clean_matches_df(row:pd.Series)-> pd.Series:
    team_1 = row['team_1']
    team_2 = row['team_2']
    if len(team_1) > 0:
        if '(' in team_1[-1]:
            player_b = team_1[-1]
            team_1 = [team_1[0],player_b[:player_b.index("(")-1]]
            row['team_1'] = team_1
    if len(team_2) > 0:  
        if '(' in team_2[-1]:
            player_b = team_2[-1]
            team_2 = [team_2[0],player_b[:player_b.index("(")-1]]
            row['team_2'] = team_2
            
    row['winner'] = row[row['winner']]
    return row


def prizes_calc(row: pd.Series)-> pd.Series:
    # print(row)
    player_list = row['team_1'] + row['team_2']
    
    prizes_dict = {'FINALS':{'winners': 52500, 'Final': 30000,'thirds': 21000, 'fourths':13500, 'Quarterfinals':7688},
        'MAJOR': {'winners': 47250, 'Final': 23625, 'Semifinals': 13125, 'Quarterfinals':8531, 'Round of 16': 5250, 'Round of 32': 2953, 'Round of 64':1477, 'Q2': 820}, 
        'P1': {'winners': 25500, 'Final': 13500, 'Semifinals': 7125, 'Quarterfinals':4500, 'Round of 16': 2625, 'Round of 32': 1922, 'Round of 64':1266, 'Q2': 1266}, 
        'P2': {'winners': 15000, 'Final': 8250, 'Semifinals': 4500, 'Quarterfinals':3000, 'Round of 16': 1781, 'Round of 32': 891, 'Q3': 563 }}
    pattern = '(FINALS|MAJOR|P1|P2)'
    event_category = re.search(pattern, row['event_title']).group(0)
    round_name = row['round_name']
    list_of_rows = []
    if round_name in prizes_dict[event_category].keys():
        for player in player_list:
            if player not in row['winner']: 
                if event_category != 'FINALS':
                    prize = prizes_dict[event_category][round_name]
                    list_of_rows.append({'player': player, 'prize':prize})
                else: 
                    prize = prizes_dict[event_category]['fourths']
                    list_of_rows.append({'player': player, 'prize':prize})
            
            else:
                if round_name == 'Final':
                    prize = prizes_dict[event_category]['winners']
                    list_of_rows.append({'player': player, 'prize':prize})
                    
                elif round_name == 'Final 3rd place':
                    prize = prizes_dict[event_category]['thirds']
                    list_of_rows.append({'player': player, 'prize':prize})
        df_to_return = pd.DataFrame(list_of_rows)
        return df_to_return
    else: return None


def loc_split(row):
    city, country = row['location'].split(' - ')
    pattern = '(FINALS|MAJOR|P1|P2)'
    category = re.search(pattern, row['title']).group(0)
    return pd.Series(index=('city', 'country', 'category'), data=(city, country, category))


def transform(path: str):
    path = './output_scrap/Men_events.json'
    matches, tournaments = extract_data(path)
    df_matches = pd.DataFrame(matches)
    df_matches_cleaned = df_matches.apply(axis=1, func=clean_matches_df)
    df_final_round = df_matches_cleaned.copy()[df_matches_cleaned['round_name'] == 'Final']
    df_final_round['winner'] = df_final_round.loc[:,'winner'].map(lambda x: ', '.join(x))
    wins_count = df_final_round.groupby('winner')['winner'].count().reset_index(name='counts')
    
    prizes_df = pd.concat(df_matches_cleaned.apply(axis=1, func=prizes_calc).dropna().to_list(), ignore_index=True)
    prizes_sum = prizes_df.groupby('player').sum('prize').sort_values(by= 'prize',ascending=False)
    
    
    df_tournaments = pd.DataFrame(tournaments)
    df_tournaments[['city', 'country', 'category']] = df_tournaments.apply(func=loc_split, axis=1)
    
    return (wins_count, prizes_sum, df_tournaments)