from plugins.scrap.scrap import run
from plugins.transform.transform import transform
from plugins.load.load import table_creator
from sqlalchemy import create_engine

import os
import json


url_engine = os.environ['POSTGRES_URL']  # POSTGRES DB CREDENTIALS
url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year="#PAGE TO SCRAP


gender = "Women" #Men or Women
organization = "PP" #Premier Padel
year = "2024"
path_scrap = f'./output_scrap/{organization}_{gender}_{year}.json'
path_transform = f'./output_transform/{year}_{gender}'
if __name__ == "__main__":
    # Scraping data
    list_events = run(url + year, gender)
    json.dump(list_events, open(path_scrap, "w"))
    
    # Transforming Data
    matches_cleaned,tournament_winner, prizes,  tournaments = transform(path_scrap, gender)
    
    # Saving data in files
    matches_cleaned.to_csv(f'{path_transform}_matches_cleaned.csv', index=False)
    tournament_winner.to_csv(f'{path_transform}_tournament_winner.csv', index=False)
    prizes.to_csv(f'{path_transform}_prizes_df.csv', index= False)
    tournaments.to_csv(f'./output_transform/{organization}_tournaments.csv', index=False)
    
    # Data Base Engine
    eng = create_engine(url_engine)
    # Uplouding Data
    table_creator(f'{gender.lower()}_tournament_winner', tournament_winner, eng, False)
    table_creator(f'{gender.lower()}_prizes', prizes, eng)
    table_creator(f'{organization.lower()}_tournaments', tournaments, eng, False)
