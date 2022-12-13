import requests
import database
from datetime import datetime
from bs4 import BeautifulSoup as bs

db = database

class parsing(object):

    def __init__(self):
        super(parsing, self).__init__()

    @staticmethod
    def chec_connection():
        headers = {'accept': '*/*',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

        time = str(datetime.today().hour) + ":" + str(datetime.today().minute)

        try:
            request_session = requests.Session()
            requestGismeteo = request_session.get('https://www.gismeteo.ru/weather-moskovskiy-167398/now/', headers=headers)
            requestYandex = request_session.get('https://yandex.ru/pogoda/?lat=55.60214996&lon=37.34654999', headers=headers)

            if (requestGismeteo.status_code == 200):

                db.database.creating_database(datetime.today().day, datetime.today().month, datetime.today().year,
                    time, status="Успешно", temperature=parsing.parsing_temp(requestYandex),
                    status_weat=parsing.parsing_status(requestGismeteo), speed_wind=parsing.parsing_wind(requestYandex))

        except ConnectionError:
            db.database.creating_database(datetime.today().day, datetime.today().month, datetime.today().year,
                    time, status="None", temperature="None", status_weat="None", speed_wind="None")

    @staticmethod
    def parsing_temp(request):
        soup = bs(request.text, "html.parser")
        temp = soup.find_all("div", class_="temp fact__temp fact__temp_size_s")  # температура яндекс
        for temperature in temp:
            temp = "" + str(temperature.text)
        return temp

    @staticmethod
    def parsing_status(request):
        soup = bs(request.text, "html.parser")
        temp = soup.find_all('div', class_='now-desc')              # статус погоды
        for status_weat in temp:
            status = "" + str(status_weat.text)
        return status

    @staticmethod
    def parsing_wind(request):
        soup = bs(request.text, "html.parser")
        temp = soup.find_all("span", class_="wind-speed")  # скорость ветра
        for temperature in temp:
            wind = "" + str(temperature.text)
        return (wind + " м/с")



if __name__ == '__main__':
    pars = parsing()
    pars.chec_connection()

