
import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 

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
    session = Session(engine)
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    lastdate = session.query(measurement.date).order_by(measurement.date.desc()).first()
    lastyear = (dt.datetime.strptime(lastdate[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= lastyear).all()
    
    datedata= []
    for measurement.date, measurement.prcp in prcp_data:
        prcp_data_dic= {}
        prcp_data_dic["date"]= measurement.prcp
        datedata.append(prcp_data_dic)
    
# Return the JSON representation of your dictionary.
    return jsonify(datedata)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
#Return a JSON list of stations from the dataset
    
    stations= session.query(stations.station).all()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
#Query the dates and temperature observations of the most active station for the last year of data.
    lastdate = session.query(measurement.date).order_by(measurement.date.desc()).first()
    lastyear = (dt.datetime.strptime(lastdate[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    top_temp_obs = session.query(measurement.date, measurement.tobs).filter(measurement.date >= lastyear).filter(measurement.station == 'USC00519281').all()

#Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(top_temp_obs)

@app.route("/api/v1.0/<start>")

def start(start_date):
    session = Session(engine)
    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date)

    


@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start_date, end_date):
    session = Session(engine)

    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

# function usage example
    # return(calc_temps('2015-05-12', '2015-05-18'))
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.










if __name__ == '__main__':
    app.run(debug=True)