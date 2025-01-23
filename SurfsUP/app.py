# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine
import datetime as dt

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
# reflect the tables
Base.classes.keys()

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Homepage

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation analysis
 
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).\
        order_by(measurement.date).all()

    session.close()

    all_measures = []
    for d, p in precip:
        last_12_mo_precip = {}
        last_12_mo_precip[d] = p
        all_measures.append(last_12_mo_precip)

    return jsonify(all_measures)

# List of stations

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    list_stations = session.query(station.station, station.name).all()
    
    session.close()
    
    all_stations = []
    for s, n in list_stations:
        station_dict = {}
        station_dict[s] = n
        all_stations.append(station_dict)

    return jsonify(all_stations)

# Dates and temperature observations/ Most active station, previous year

@app.route("/api/v1.0/tobs")
def tobs():

    most_active_station = 'USC00519281'

    session = Session(engine)

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    most_active_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= previous_year).\
        filter(measurement.station == most_active_station).all()

    most_active_list = []
    for d, t in most_active_data:
        most_active_temp_data = {}
        most_active_temp_data[d] = t
        most_active_list.append(most_active_temp_data)

    return jsonify(most_active_list)

# Start Date

# Start and End Date


if __name__ == "__main__":
    app.run(debug=True)


 


    
     