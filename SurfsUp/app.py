# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():

    """List all available api routes."""
    return (
        f"<b>Welcome to Honolulu, Hawaii Climate API</b><br/></br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/2016,2,23<br>"
        f"/api/v1.0/start/2016,3,23/end/2017,5,31<br/></br>"
        f"You can change the date to your liking while keeping it in the yyyy-m-d format")



@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Perform query from 2016, 8, 23 and later, sorts the date in ascending order,
    then returns everything in a list, where each date and percipitation is in a dictionary format"""

    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > dt.date(2016,8,22)).\
    order_by(measurement.date).all()
    session.close()

    rain=[]
    for date, prcp in results:
        rain_dict = {}
        rain_dict["Date"] = date
        rain_dict["Precipitation"] = prcp
        rain.append(rain_dict)

    return jsonify(rain)



@app.route("/api/v1.0/stations")
def station_list():
    """ Fetch the name of all the stations and returns it in a list format"""
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def temperature():

    """ Perform query from 2016, 8, 23 and later for station USC00519281, sorts the date in ascending order,
        then returns everything in a list, where each date and temperature is in a dictionary format"""

    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= dt.date(2016, 8 ,23)).\
            filter(measurement.station =='USC00519281')
    session.close()

    temp=[]
    for date, tobs in results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temp.append(temp_dict)
    
    return jsonify(temp)



@app.route("/api/v1.0/start/<start>")
def start_date(start):
    """Performs a query that is greater than or equal to the inputed start date, and
    returns the min, max, and avg temperature in a list """

    session = Session(engine)
    sel = [func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]

    results = session.query(*sel).filter(func.strftime('%Y-%m-%d', measurement.date) >= start).all()
    session.close
    
    temp = list(np.ravel(results))

    return jsonify(temp)



@app.route("/api/v1.0/start/<start>/end/<end>")
def start_end_date(start, end):
    """Performs a query that is greater than or equal to the inputed start date, and less than and equal to 
    the end date. Then returns the min, max, and avg temperature in a list """
    
    session = Session(engine)
    sel = [func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)]

    results = session.query(*sel).filter(func.strftime('%Y-%m-%d', measurement.date) >= start).\
            filter(func.strftime('%Y-%m-%d', measurement.date) <= end).all()
    session.close

    temp = list(np.ravel(results))

    return jsonify(temp)
        


if __name__ == '__main__':
    app.run(debug=True)