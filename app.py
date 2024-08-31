import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import fastf1
from fastf1 import plotting
import pandas as pd

fastf1.Cache.enable_cache('cache')  # Enable caching

app = dash.Dash(__name__)
app.title = "Live F1 Race Dashboard"

app.layout = html.Div([
    html.H1('Live F1 Race Data Dashboard'),
    html.Div([
        dcc.Graph(id='live-race-data'),
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # Update every 30 seconds
            n_intervals=0
        )
    ], className='container')
], className='main-container')



@app.callback(
    Output('live-race-data', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):

    session = fastf1.get_session(2023, 'Monaco', 'R')  # Example: Monaco GP 2023 Race
    session.load()
    
    laps = session.laps
    lap_times = laps[['Driver', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']]
    
    fig = go.Figure()

    for driver in lap_times['Driver'].unique():
        driver_laps = lap_times[lap_times['Driver'] == driver]
        fig.add_trace(go.Scatter(
            x=driver_laps.index, y=driver_laps['LapTime'].dt.total_seconds(),
            mode='lines+markers', name=driver
        ))

    fig.update_layout(title='Lap Times by Driver', xaxis_title='Lap Number', yaxis_title='Lap Time (s)')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
