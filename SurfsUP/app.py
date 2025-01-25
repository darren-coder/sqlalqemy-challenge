# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
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
        f"Enter a start date to retrieve tobs information<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"Enter start date/end date for tobs information<br/>"
        f"/api/v1.0/start_date/end_date/<start_date>/<end_date>"
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

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    session = Session(engine)

    most_active_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= previous_year).\
        filter(measurement.station == most_active_station).all()

    most_active_temp_list = []
    for d, t in most_active_data:
        most_active_temp_data = {}
        most_active_temp_data[d] = t
        most_active_temp_list.append(most_active_temp_data)

    return jsonify(most_active_temp_list)

# Start Date

@app.route("/api/v1.0/start_date/<start_date>")
def start_from(start_date):
    """Temperature observations from Date entered."""
    
    session = Session(engine)

    tobs_from = session.query(measurement.date, 
                              func.min(measurement.tobs),\
                              func.avg(measurement.tobs),\
                                func.max(measurement.tobs)).\
                                filter(measurement.date >= start_date).\
                                group_by(measurement.date)

    session.close()

    tobs_from_list = []
    for d, min, avg, max in tobs_from:
        tobs_from_data = {}
        tobs_from_data["Date"] = d
        tobs_from_data["Minimum Temperature"] = min
        tobs_from_data["Average Temperature"] = round(avg, 1)
        tobs_from_data["Maximum Temperature"] = max
        tobs_from_list.append(tobs_from_data)

    return jsonify(tobs_from_list)

# Start and End Date

@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
def start_end(start_date, end_date):
    
    session = Session(engine)

    tobs_from_to = session.query(measurement.date, 
                              func.min(measurement.tobs),\
                              func.avg(measurement.tobs),\
                                func.max(measurement.tobs)).\
                                filter(measurement.date >= start_date).\
                                filter(measurement.date <= end_date).\
                                group_by(measurement.date).all()

    session.close()

    tobs_from_to_list = []
    for date, min, avg, max in tobs_from_to:
        tobs_from_to_list.append({
            "Date": date,
            "Minimum Temperature": min,
            "Average Temperature": round(avg, 1),
            "Maximum Temperature": max
        })


    return jsonify(tobs_from_to_list)


if __name__ == "__main__":
    app.run(debug=True)


 


    
     