# Import Dependencies
import numpy as np
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


## Database Setup ##
# Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

## Flask Setup ##
app = Flask(__name__)


# Flask Routes

@app.route("/")
def welcome():
    #List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )

 

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    all_date = []
    for date, prcp in results:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["prcp"] = prcp
        all_date.append(dates_dict)

    #Return the JSON representation of your dictionary.
    return jsonify(all_date) 



@app.route("/api/v1.0/stations")
def stations():
    ## Return a JSON list of stations from the dataset.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Find the latest date and the date 1 year before that
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #latest date returns 2017-08-23 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Find the most active station from the last year of data
    station_most_last_year = session.query(Measurement.station).\
        filter(Measurement.date >= year_ago).\
        group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
        #returns 'USC00519397'

    # Query the dates and temperature observations of the most 
    #active station for the last year of data.
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.station == 'USC00519397').\
        order_by(Measurement.date).all()

    session.close()
    #Return the JSON representation of your dictionary.
    latest_year_date = []
    for date, tobs in results:
        latest_year_dict = {}
        latest_year_dict["date"] = date
        latest_year_dict["tobs"] = tobs
        latest_year_date.append(latest_year_dict)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(latest_year_date) 

    

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query for the min temp, avg temp, max temp from a given start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    session.close()

    #Convert results into a dictionary
    start_stats = []
    for min, avg, max in results:
        start_dict = {}
        start_dict["Min Temp"] = min
        start_dict["Avg Temp"] = avg
        start_dict["Max Temp"] = max
        start_stats.append(start_dict)

    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the max temperature for a given start date
    return jsonify(start_stats)

    

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query for the min temp, avg temp, max temp from a given start date to a given end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    session.close()

    #Convert results into a dictionary
    start_end_stats = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["Min Temp"] = min
        start_end_dict["Avg Temp"] = avg
        start_end_dict["Max Temp"] = max
        start_end_stats.append(start_end_dict)

    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the max temperature for a given start and end date
    return jsonify(start_end_stats)



if __name__ == '__main__':
    app.run(debug=True)
