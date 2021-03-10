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
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
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

    




@app.route("/api/v1.0/&lt;start&gt;")
def start():
    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the max temperature for a given start or start-end range.
    return(f"start date data")
    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
    #for all dates greater than and equal to the start date.




@app.route("/api/v1.0/&lt;start&gt;/&lt;end&gt;")
def start_end():
    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the max temperature for a given start or start-end range.
    return(f"Data between start and end date")

    #When given the start and the end date, calculate the `TMIN`, `TAVG`, 
    #and `TMAX` for dates between the start and end date inclusive.



if __name__ == '__main__':
    app.run(debug=True)
