from plugins.scrap.scrap import run
from plugins.transform.transform import transform
from plugins.load.load import table_creator
from sqlalchemy import create_engine

import os
import json
# import pandas
url_engine = os.environ['URL_ENGINE']
url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year="
gender_arg = "Men" #Men or Women
path = f'./output_scrap/{gender_arg}_events.json'
output_transform = './output_transform'
if __name__ == "__main__":
    list_events = run(url + "2024", gender_arg)
    json.dump(list_events, open(path, "w"))
    wins_count, prizes_sum, df_tournaments = transform(path)
    wins_count.to_csv(f'{output_transform}/wins_count.csv', index=False)
    prizes_sum.to_csv(f'{output_transform}/prizes_sum.csv')
    df_tournaments.to_csv(f'{output_transform}/tournaments.csv', index=False)
    eng = create_engine(url_engine)
    table_creator('wins_count', wins_count, eng, False)
    table_creator('prizes_sum', prizes_sum, eng)
    table_creator('df_tournaments', df_tournaments, eng, False)
