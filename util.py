# -*- coding: utf-8 -*-
from darksky import forecast
from datetime import date, timedelta
import pandas as pd
import os

ROOT_DIR = "%s/forecast_weather_flask" % os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

def initDir():
    if not os.path.isdir("%s/%s" % (ROOT_DIR, "csvs")):
        os.mkdir("%s/%s" % (ROOT_DIR, "csvs"))

def main():
    initDir()
    
    cities = dict([("SP", (-23.5505, -46.6333)), ("RJ", (-22.9068, -43.1729))])
    totalCities = []

    for key, value in cities.items():
        tCity = forecastOfWeek(key, cities[key])
        for c in tCity:
            totalCities.append(c)

    createCsv(totalCities, ["Date", "City", "MinTemp", "MaxTemp"])

    return totalCities

def forecastOfWeek(city, geo):
    days = []
    weekday = date.today()
    with forecast("d4f466aaa280fb79c009d11851c638a4", *geo) as sp:
        for day in sp.daily:
            day = [
                date.strftime(weekday, "%d/%b/%Y"),
                city,
                int((day.temperatureMin - 32) / 1.8),
                int((day.temperatureMax - 32) / 1.8),
            ]
            weekday += timedelta(days=1)
            days.append(day)
    
    return days


def createCsv(data, columns=None):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(
        "csvs/data_%s.csv" % (str(date.today()).replace("-", "_")),
        header=True,
        index=False,
        sep=";",
    )
