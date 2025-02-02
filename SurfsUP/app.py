# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func

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
        f"Enter a start date after url below to retrieve tobs information "
        f"using this format: /YYYY-MM-DD<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"Enter start date/end date after url below for tobs information "
        f"using this format: /YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"/api/v1.0/start_date/end_date/<start_date>/<end_date>"
    )

# Precipitation analysis
 
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Previous year of temperature observations."""
    
    # import datetime
    
    import datetime

    # Select Dates    
    
    previous_year = datetime.date(2017,8,23) - datetime.timedelta(days=365)
    
    # Open session / make query / close session

    session = Session(engine)

    precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).\
        order_by(measurement.date).all()

    session.close()

    # create and return jsonify list

    all_measures = []
    for d, p in precip:
        last_12_mo_precip = {}
        last_12_mo_precip[d] = p
        all_measures.append(last_12_mo_precip)

    return jsonify(all_measures)

# List of stations

@app.route("/api/v1.0/stations")
def stations():
    """List of stations."""
    
    # Session and Query

    session = Session(engine)

    list_stations = session.query(station.station, station.name).all()
    
    session.close()

    # Create list and return jsonify to url

    all_stations = []
    for s, n in list_stations:
        station_dict = {}
        station_dict[s] = n
        all_stations.append(station_dict)

    return jsonify(all_stations)

# Dates and temperature observations/ Most active station, previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    """Previous year of temperature observations from busiest station."""
    # import datetime
    
    import datetime

    # Set variables

    most_active_station = 'USC00519281'

    previous_year = datetime.date(2017,8,23) - datetime.timedelta(days=365)

    # Session and Query

    session = Session(engine)

    most_active_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= previous_year).\
        filter(measurement.station == most_active_station).all()

    session.close()

    # Create list and return jsonify to url.

    most_active_temp_list = []
    for d, t in most_active_data:
        most_active_temp_data = {}
        most_active_temp_data[d] = t
        most_active_temp_list.append(most_active_temp_data)

    return jsonify(most_active_temp_list)

# Start Date temperature observations.

@app.route("/api/v1.0/start_date/<start_date>")
def start_from(start_date):
    """Temperature observations from Date entered."""

    # import datetime

    from datetime import datetime

    # Set variable for date

    start_object = datetime.strptime(start_date, "%Y-%m-%d").date()
    print(start_object)

    # Session and Query

    session = Session(engine)

    sel =  [func.min((measurement.tobs).label('Minimum Temp')),
           func.avg((measurement.tobs).label('Average Temp')),
           func.max((measurement.tobs).label('Maximum Temp'))]
    
    start = session.query(*sel).\
        filter(measurement.date >= start_object)
    
    session.close()

    # Create list and return jsonify to url.

    tobs_from_list = []
    for min, avg, max in start:
        tobs_from_data = {}
        tobs_from_data["Minimum Temperature"] = min
        tobs_from_data["Average Temperature"] = round(avg, 1)
        tobs_from_data["Maximum Temperature"] = max
        tobs_from_list.append(tobs_from_data)

    return jsonify(tobs_from_list)

# Start and End Date temperature observations.

@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """Temperature observations within given date range"""

    # import datetime

    from datetime import datetime

    # Set variables for dates.

    start_object = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_object = datetime.strptime(end_date, "%Y-%m-%d").date()
    print(start_object)
    print(end_object)
    
    # Session and Query.

    session = Session(engine)

    sel =  [func.min((measurement.tobs).label('Minimum Temp')),
           func.avg((measurement.tobs).label('Average Temp')),
           func.max((measurement.tobs).label('Maximum Temp'))]
    
    start_to_end = session.query(*sel).\
        filter(measurement.date >= start_object,
               measurement.date <= end_object).all()
    
    session.close()

    # Create list and return jsonify to url.
    
    tobs_from_to_list = []
    for  min, avg, max in start_to_end:
        tobs_from_to_data = {}
        tobs_from_to_data["Minimum Temperature"] = min
        tobs_from_to_data["Average Temperature"] = round(avg, 1)
        tobs_from_to_data["Maximum Temperature"] = max
        tobs_from_to_list.append(tobs_from_to_data)

    return jsonify(tobs_from_to_list)

# Entry point check

if __name__ == "__main__":
    app.run(debug=True)


 


    
     