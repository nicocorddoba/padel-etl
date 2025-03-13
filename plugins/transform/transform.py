import pandas as pd
import json
import re

def extract_data(path: str) -> list[dict]:
    # Data extraction from json file alocated in './output_scrap' folder
    try: 
        with open (path, encoding='utf-8') as f:
            raw_data = json.load(f)
            f.close()

        matches = [] # All matches from {organization (Premier Padel)}
        tournaments = [] # All tournaments from {organization (Premier Padel)}
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
    """function maded to use within an .apply from pandas.DataFrame
    with these required columns:
    team_1 (Array): first pair of a padel match
    team_2 (Array): second pair of a padel match
    winner (String): the winner team ('team_1' or 'team_2')
    event_title (String): the title of each premier padel tournament
    
    Args:
        row (pd.Series): each row from pandas.DataFrame

    Returns:
        row (pd.Series): The transformed row
    """
    team_1 = row['team_1']
    team_2 = row['team_2']
    # In some rows, there's the ranking number of the first 16 pairs
    # or '(Q)' that means that pair comes from qualy rounds
    # we are not going to use it, so we'll delete
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
    pattern = '(FINALS|MAJOR|P1|P2)'
    event_category = re.search(pattern, row['event_title']).group(0)
    row['category'] = event_category
    return row


def prizes_calc(row: pd.Series, gender:str)-> pd.Series:
    player_list = row['team_1'] + row['team_2']
    if gender == 'Men':
        prizes_dict = {'FINALS':{'winners': 52500, 'Final': 30000,'thirds': 21000, 'Final 3rd place':13500, 'Quarterfinals':7688},
            'MAJOR': {'winners': 47250, 'Final': 23625, 'Semifinals': 13125, 'Quarterfinals':8531, 'Round of 16': 5250, 'Round of 32': 2953, 'Round of 64':1477, 'Q2': 820}, 
            'P1': {'winners': 25500, 'Final': 13500, 'Semifinals': 7125, 'Quarterfinals':4500, 'Round of 16': 2625, 'Round of 32': 1922, 'Q2': 1266}, 
            'P2': {'winners': 15000, 'Final': 8250, 'Semifinals': 4500, 'Quarterfinals':3000, 'Round of 16': 1781, 'Round of 32': 891, 'Q3': 563 }}
    else:
        prizes_dict = {'FINALS':{'winners': 52500, 'Final': 30000,'thirds': 21000, 'fourths':13500, 'Quarterfinals':7688},
            'MAJOR': {'winners': 47250, 'Final': 23625, 'Semifinals': 13125, 'Quarterfinals':8531, 'Round of 16': 5250, 'Round of 32': 2953, 'Round of 64':1477, 'Q2': 820}, 
            'P1': {'winners': 17000, 'Final': 9350, 'Semifinals': 5100, 'Quarterfinals':3400, 'Round of 16': 2019, 'Round of 32': 1009, 'Q2': 638}, 
            'P2': {'winners': 8500, 'Final': 4675, 'Semifinals': 2550, 'Quarterfinals':1700, 'Round of 16': 1009, 'Round of 32': 673, 'Q3': 319 }}
        
    event_category = row['category']
    round_name = row['round_name']
    row_list = []
    if round_name in prizes_dict[event_category].keys():
        for player in player_list:
            if player not in row['winner']: 
                if event_category != 'FINALS' or round_name != 'Final 3rd place':
                    prize = prizes_dict[event_category][round_name]
                    row_list.append({'player': player, 'prize':prize, 'tournament':row['event_title'], 'category': event_category})
                else: 
                    prize = prizes_dict[event_category]['Final 3rd place']
                    row_list.append({'player': player, 'prize':prize, 'tournament':row['event_title'], 'category': event_category})
            else:
                if round_name == 'Final':
                    prize = prizes_dict[event_category]['winners']
                    row_list.append({'player': player, 'prize':prize, 'tournament':row['event_title'], 'category': event_category})
                elif round_name == 'Final 3rd place':
                    prize = prizes_dict[event_category]['thirds']       
                    row_list.append({'player': player, 'prize':prize, 'tournament':row['event_title'], 'category': event_category})

        df_to_return = pd.DataFrame(row_list)
        return df_to_return
    else: return None


def loc_split(row):
    city, country = row['location'].split(' - ')
    pattern = '(FINALS|MAJOR|P1|P2)'
    category = re.search(pattern, row['title']).group(0)
    return pd.Series(index=('city', 'country', 'category'), data=(city, country, category))


def transform(path_scrap: str, gender:str):
    matches, tournaments = extract_data(path_scrap)
    df_matches = pd.DataFrame(matches)
    df_matches_cleaned = df_matches.apply(axis=1, func=clean_matches_df)
    df_final_round = df_matches_cleaned.copy()[df_matches_cleaned['round_name'] == 'Final']
    df_final_round['winner'] = df_final_round.loc[:,'winner'].map(lambda x: ', '.join(x))

    winners = df_final_round[['winner', 'event_title', 'category']]
    prizes_df = pd.concat(df_matches_cleaned.apply(axis=1, func=prizes_calc, gender=gender).dropna().to_list(), ignore_index=True)
    # prizes_sum = prizes_df.groupby('player').sum('prize').sort_values(by= 'prize',ascending=False)
    
    
    df_tournaments = pd.DataFrame(tournaments)
    df_tournaments[['city', 'country', 'category']] = df_tournaments.apply(func=loc_split, axis=1)
    
    return (df_matches_cleaned,winners, prizes_df, df_tournaments)