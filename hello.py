from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd
import json
import plotly

def hello(environment):
    """Return a friendly HTTP greeting."""

    df = pd.read_csv('2014_world_gdp_with_codes.csv')

    fig = go.Figure(data=go.Choropleth(
        locations = df['CODE'],
        z = df['GDP (BILLIONS)'],
        text = df['COUNTRY'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = 'GDP<br>Billions US$',
    ))

    fig.update_layout(
        title_text=f'2014 Global GDP on {environment}',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                CIA World Factbook</a>',
            showarrow = False
        )]
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('attempt_at_plotly.html', graphJSON=graphJSON)