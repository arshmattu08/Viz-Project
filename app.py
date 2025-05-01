#imports
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, callback, State

# app code
app = Dash(__name__)
app.title = "Powerlifting Viz App" 



if (__name__ == '__main__'):
    app.run_server(debug= True)
