from plugins.scrapp.scrapp import run

url = "https://www.padelfip.com/es/calendario-premier-padel/?events-year="
gender = "male" #MEN or WOMEN#

if __name__ == "__main__":
    run(url + "2024", gender)