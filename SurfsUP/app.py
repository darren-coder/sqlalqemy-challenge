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
        f"/api/v1.0/precipitation<br/"
        f"/api/v1.0/stations<br/"
        f"/api/v1.0/tobs<br/"
        f"/api/v1.0/<start><br/"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation analysis
 
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    most_recent = session.query(measurement.date).\
    order_by(measurement.date.desc()).first()
    str_recent = most_recent[0]

    most_recent_date = dt.datetime.strptime(str_recent, '%Y-%m-%d').date()

    one_year = most_recent_date - dt.timedelta(days=365)

    precip = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= one_year).\
    order_by(measurement.date).all()

    session.close()

    all_measures = []
    for d, p in precip:
        last_12_mo_precip = {}
        last_12_mo_precip[0] = p
        last_12_mo_precip[1] = d
        all_measures.append(last_12_mo_precip)

    return jsonify(all_measures)

# 

if __name__ == "__main__":
    app.run(debug=True)


 


    
     