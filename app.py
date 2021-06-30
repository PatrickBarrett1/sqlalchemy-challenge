import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect into new model
base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station

#
session = Session(engine)

# create an app
app = Flash(__climate_starter__)

@app.route('/')
def home():
    """List all available api routes"""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# convert query results to a dict ussing date as key and prcp as value
@app.route('/api/v1.0/precipitation')
def prcp():
     # query measurement
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date)

    # crete dict
    prcp_date = []
    for row in results:
        prcp_dict = {}
        prcp_dict['date'] = row.date
        prcp_dict['prcp'] = row.prcp
        prcp_date.append(prcp_dict)

    return jsonify(prcp_date)

# return a JSON list of stations from the dataset
@app.route('/api/v1.0/station')
def stations():
     # query measurement
    results = session.query(station.name).all()

    # covert to list
    station_list = list(results)

    return jsonify(station_list)


# query the dates and temperature observations of the most active station for the last year of data
@app.route('/api/v1.0/tobs')
def tobs():
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    most_active_station = active_stations[0][0]
    last_year_temps = session.query(measurement.station, measurement.tobs).filter(measurement.station == most_active_station).filter(measurement.date >= str(last_year_date)).all()

    tobs_list = list(last_year_temps)
    return jsonify(tobs_list)


# return json list of min, max, avg temp for given start - end range
# Calc min, max, avg for dates greater than or equal to start date
app.route('/api/v1.0/<start>')
def start_date(start):
    start_date = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    start_date_list = list(start_date)

    return jsonify(start_date_list)


# return json list of min, max, avg temp for given start - end range
# Calc min, max, avg for date between start and end date
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    start_end_date = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()

    start_end_list = list(start_end_date)

    return jsonify(start_end_list)


if __name__ == '__climate_stater__':
    app.run(debug=True)