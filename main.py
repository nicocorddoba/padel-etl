from plugins.scrap.scrap import run
from plugins.transform.transform import transform
import json
# import pandas

url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year="
gender_arg = "Men" #Men or Women
path = f'./output_scrap/{gender_arg}_events.json'
output_transform = './output_transform'
if __name__ == "__main__":
    list_events = run(url + "2024", gender_arg)
    json.dump(list_events, open(path, "w"))
    wins_count, prizes_sum, df_tournaments = transform(path)
    wins_count.to_csv(f'{output_transform}/wins_count.csv')
    prizes_sum.to_csv(f'{output_transform}/prizes_sum.csv')
    df_tournaments.to_csv(f'{output_transform}/tournaments.csv')