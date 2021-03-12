# sqlalchemy-challenge

In this project, I will be analyzing the climate in Honolulu Hawaii. The following will detail what this analysis includes.


## Part 1 - Climate Analysis and Exploration

To begin, I used Python and SQLAlchemy to do basic climate analysis and data exploration of my climate database. All of the following analysis is completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* First, I imported all necessary dependencies. Then, I reflected the tables into SQLAlchemy ORM using the following:

    * I used SQLAlchemy `create_engine` to connect to your sqlite database.

    * I used SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to the available classes called `Station` and `Measurement`.

    * I used `inspector` to view the column names and data types within each of the available tables.

    * I linked Python to the database by creating a SQLAlchemy session.


### Precipitation Analysis

* I started by finding the most recent date in the data set.

* Using this date, I retrieved the last 12 months of precipitation data by querying the 12 preceding months of data.

* I then selected only the `date` and `prcp` values.

* I loaded the query results into a Pandas DataFrame and set the index to the date column.

* I sorted the DataFrame values by `date`.

* Finally, I ploted the results using the DataFrame `plot` method, creating a bar chart of the precipitation in Honolulu, Hawaii over the last 12 months of data. (This can be seen at precipitation_analysis.png)

* I used Pandas to print the summary statistics for the precipitation data. (This can be seen in the climate.ipynb file at the end of the Precipitation Analysis)

### Station Analysis

* I designed a query to calculate the total number of stations in the dataset.

* Then, I designed a query to find the most active stations (i.e. which stations have the most rows?).

  * I listed the stations and observation counts in descending order.

  * Found which station id had the highest number of observations.

  * Using the most active station id, I calculated the lowest, highest, and average temperature. I did this using functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in my queries.

* I designed a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filtered by the station with the highest number of observations.

  * Queried the last 12 months of temperature observation data for this station.

  * Plotted the results as a histogram with `bins=12`. (This histogram can be seen at MostPopStationTemps_Histogram.png)

Finally, I made sure to close out my open session.

(All Climate Analysis and Exploration code can be found at climate.ipynb)

- - -

## Part 2 - Climate App

Now that I have completed my initial analysis, I designed a Flask API based on the queries that I just developed. 

* I used Flask to create my routes, described below.

### Routes

* `/`

  * Home page.

  * Lists all routes that are available.

* `/api/v1.0/precipitation`

  * Converts the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Returns the JSON representation of my dictionary.

* `/api/v1.0/stations`

  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Queries the dates and temperature observations of the most active station for the last year of data.

  * Returns a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculates the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

(All Climate app code can be found in app.py)