
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask jsonify 

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= lastyear).all()

    prcp_data_dic= {measurementdate: measurement.prcp}

    return jasonify 
# Return the JSON representation of your dictionary.


@app.route("/api/v1.0/stations")
def stations():
#Return a JSON list of stations from the dataset
    
    stations= session.query(stations.station).all()

    return jasonify (stations)

@app.route("/api/v1.0/tobs")
def temps():
#Query the dates and temperature observations of the most active station for the last year of data.
  top_temp_obs = session.query(measurement.date, measurement.tobs).filter(measurement.date >= lastyear).filter(measurement.station == 'USC00519281').all()

#Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(top_temp_obs)

@app.route("/api/v1.0/<start>")
def
@app.route("/api/v1.0/<start>/<end>")
def

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
