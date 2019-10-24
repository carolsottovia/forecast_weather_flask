# Dark Sky - Flask

This  library for the `Dark Sky
API <https://darksky.net/dev/docs>` provides access to detailed
weather information from around the globe.

[Flask](http://flask.pocoo.org/):
a micro web framework written in Python <br>

Requirements
------------

Before you start using this library, you need to get your API key
<https://darksky.net/dev/register>.

Installation
-------------
You should use pip to install darkskylib, pandas and flask:

* pip install darkskylib
* pip install pandas
* pip install flask

And to remove:
* pip uninstall darkskylib
* pip uninstall pandas
* pip uninstall flask

<!-- TOC -->

- [Flask](#flask)
    - [1. API endpoint for jasonified data](#1-api)
    - [2. Render templates](#2-render-templates)
        - [2.1. Python script](#21-python-script)
        - [2.2. HTML template](#22-html-template)

<!-- /TOC -->

## 1. API

* Use Flask to create and run a server
* Define endpoints using Flask's @app.route decorator
* Execute database queries on behalf of the client

```python

from flask import Flask, render_template
import util

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('table.html', data=util.main())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
```
## 2. Render templates

Files

- [app.py](flask/app.py)
- [templates/base.html](flask/templates/base.html)
- [templates/table.html](flask/templates/table.html)

### 2.1. Python script

```python

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
~~~~~~~~~

The forecast of week can receive weather forecast in any location on the earth. 
The flexible algorithm of weather calculation provides weather data not only 
for cities but for any geographic coordinates (latitude and longitude) and 
can get a forecast data for the next 7 days.

Parameters:
*  **key** - Your API key from https://darksky.net/dev/.
*  **geo** - The geographic coordinates: latitude and longitude of the location for the forecast
*  **date** - The forecast data for the next 7 days
*  **city** - The geographic coordinates (geo)
*  **mintemp** - The minimun temperature in Celsius
*  **maxtemp** - The maximun temperature in Celsius
~~~~~~~~~~~~~
```

### 2.2. HTML template

```html

<!doctype html>
<title>{% block title %}Home{% endblock %} - Forecast Weather</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">

<body>
  {% block content %}

</body>
 <div class="container">
  <div class="row">
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
      <h1>Forecast Weather for the next 7 days</h1>
    </div>
    <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 table-custom">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">City</th>
            <th scope="col">MinTemp</th>
            <th scope="col">MaxTemp</th>
          </tr>
        </thead>
        <tbody>
          {% for d in data %}
          <tr>
            <th>{{d[0]}}</th>
            <td>{{d[1]}}</td>
            <td>{{d[2]}} ºC</td>
            <td>{{d[3]}} ºC</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
 </div>
</body>
{% endblock %}
```

For Data Engineers
------------------

The csvs folder is created

~~~~~~~~~~~~~~~~~~
.. code:: python

import pandas as pd
import os

ROOT_DIR = "%s/forecast_weather_flask" % os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

def initDir():
    if not os.path.isdir("%s/%s" % (ROOT_DIR, "csvs")):
        os.mkdir("%s/%s" % (ROOT_DIR, "csvs"))
        

And the csv files are stored in csvs folder per day.

.. code:: python
    
def createCsv(data, columns=None):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(
        "csvs/data_%s.csv" % (str(date.today()).replace("-", "_")),
        header=True,
        index=False,
        sep=";",
    )
~~~~~~~~~~~~~~~~~~

Example script
--------------
~~~~~~~~~~~~~~~~~~
.. code:: python

from darksky import forecast
from datetime import date, timedelta
import pandas as pd

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
~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~
Output:

::

Date;City;MinTemp;MaxTemp
20/Oct/2019;SP;14;21
21/Oct/2019;SP;13;21
22/Oct/2019;SP;15;25
23/Oct/2019;SP;16;23
24/Oct/2019;SP;16;27
25/Oct/2019;SP;18;28
26/Oct/2019;SP;18;28
27/Oct/2019;SP;18;29
20/Oct/2019;RJ;20;25
21/Oct/2019;RJ;18;25
22/Oct/2019;RJ;19;27
23/Oct/2019;RJ;21;26
24/Oct/2019;RJ;21;28
25/Oct/2019;RJ;21;29
26/Oct/2019;RJ;22;29
27/Oct/2019;RJ;22;29
