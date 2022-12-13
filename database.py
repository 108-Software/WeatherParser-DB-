import sqlite3 as sql

class database(object):

    def __init__(self):
        super(database, self).__init__()

    @staticmethod
    def creating_database(day, month, year, time, status, temperature, status_weat, speed_wind):
        Month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dbase = sql.connect(str(day) + " " + Month[month-1] + " " + str(year) + ".db")
        with dbase:
            pointer = dbase.cursor()

            pointer.execute("""CREATE TABLE IF NOT EXISTS Weather(
                'Время' TEXT,
                'Статус подключения' TEXT,
                'Температура' TEXT,
                'Состояние погоды' TEXT,
                'Скорость ветра' TEXT);
                """)

            results = (time, status, temperature, status_weat, speed_wind)

            pointer.execute("INSERT INTO Weather VALUES(?, ?, ?, ?, ?);", results)
            dbase.commit()
            pointer.close()

