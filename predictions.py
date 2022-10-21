from flask import Flask, render_template
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json

from google.cloud import bigquery
# Construct a BigQuery client object.
client = bigquery.Client()

def get_stations(lat, lon):
    """Get the closest stations to the lat and long passed"""

    close_to_query = f"""
    SELECT
      name, id,
      state,
      latitude,
      longitude,
      DEGREES(ACOS(SIN(RADIANS(latitude)) * SIN(RADIANS({lat})) + COS(RADIANS(latitude)) * COS(RADIANS({lat})) * COS(RADIANS(longitude - {lon})))) * 60 * 1.515 * 1.609344 AS dist_kms
    FROM
      [bigquery-public-data:ghcn_d.ghcnd_stations]
    ORDER BY
      dist_kms ASC
    LIMIT
      1000"""

    # Set use_legacy_sql to True to use legacy SQL syntax (this is necessary to use the DEGREES function)
    job_config = bigquery.QueryJobConfig(use_legacy_sql=True)

    burlington_query_close_to = client.query(close_to_query, job_config=job_config)  # Make an API request.

    burlington_stations_close_to = burlington_query_close_to.to_dataframe()
    ## Build query
    stations_within_30_kms = list(burlington_stations_close_to[burlington_stations_close_to.dist_kms <= 30]['id'])

    stations_within_30km_text = '\', \''.join(stations_within_30_kms)

    return stations_within_30km_text

def get_the_forecast(days):
    burlington_arima_forecast_query = f"""SELECT
     *
    FROM
     ML.FORECAST(MODEL `msds-434-robords-oct.weather_prediction.burlington_snow_arima`,
                 STRUCT({days} AS horizon, 0.8 AS confidence_level))"""
    burlington_arima_forecast_365 = client.query(burlington_arima_forecast_query)  # Make an API request.
    burlington_arima_forecast_365_df = burlington_arima_forecast_365.to_dataframe()
    return burlington_arima_forecast_365_df


def get_actuals():
    stations_within_30km_text = get_stations(lat=44.47, lon=-73.15)

    burlington_2022_time_series_query = """SELECT
      date,
      AVG(value) as mean_value
    FROM
      `bigquery-public-data.ghcn_d.ghcnd_2022`
    WHERE qflag IS NULL
    AND id IN ('{}')
    AND element = 'SNOW'
    GROUP BY date
    """.format(stations_within_30km_text)

    burlington_2022_time_series_data = client.query(burlington_2022_time_series_query)

    burlington_2022_time_series_data_df = burlington_2022_time_series_data.to_dataframe()

    return burlington_2022_time_series_data_df

def prediction_chart():
    """Return a the prediction chart"""

    burlington_arima_forecast_365_df = get_the_forecast(365)

    burlington_2022_time_series_data_df = get_actuals()

    fig = px.scatter(burlington_2022_time_series_data_df, x="date", y="mean_value", title='Burlington VT Snow 2022')

    fig.add_trace(go.Scatter(x=burlington_arima_forecast_365_df["forecast_timestamp"],
                             y=burlington_arima_forecast_365_df["forecast_value"],
                             mode="lines", name='Predicted Value'))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('snow_predictions.html', graphJSON=graphJSON)