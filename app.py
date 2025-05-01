#imports
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, callback, State

# app code
app = Dash(__name__)
app.title = "Powerlifting Viz App" 

# Outer Div
app.layout = html.Div([
    html.H1("Explore Powerlifting", style={
        "position":"relative","left":"80px",
        "font-family":"Roboto, sans-serif",
        "padding":"10px 0px 10px 0px",
        "margin-bottom":"60px"}),

# Sidebar
html.Div([
        html.Button("View Dataset",style={
            "position":"relative","top":"100px",
            "padding":"12px 20px 12px 20px",
            "border-radius": "7px", 
            "background-color":"#3E44B8",
            "color":"white",
            "border": "2px solid white",
            "boxShadow": "none",  
            "cursor": "pointer",
            "font-size":"14px"}),

        html.H2("Filters", style = {
            "color":"white",
            "position":"relative","top":"140px",
            "font-size":"39px",
            "font-family":"Roboto, sans-serif"}),

        dcc.Dropdown(options=[], placeholder="Year",style = {
            "color":"white",
            "position":"relative","top":"70px","left":"12px",
            "width":"88px"
            
        }),
         dcc.Dropdown(options=[], placeholder="Age",style = {
            "color":"white",
            "position":"relative","top":"85px","left":"12px",
            "width":"88px"
            
        }),
         dcc.Dropdown(options=[
             {'label':'Male','value':'M'},
             {'label':'Female','value':'F'}
         ], placeholder="Gender",style = {
            "position":"relative","top":"100px","left":"12px",
            "width":"98px",
            "color":"black"})],
# sidebar styling
     style={
        "padding": "20px",
        "width": "10%",
        "backgroundColor": "#2E2E2E",
        "height": "100vh",
        "position": "fixed",
        "top": 0,
        "left": 0,
    }),

# Visualization Toggle Buttons
html.Div([
    html.Button("Strength Distribution", style = {
        "background-color":"transparent",
        "color":"white",
        "border-radius": "7px",
        "cursor": "pointer",
        "padding":"12px 20px 12px 20px",
        "font-size":"14px",
        "border": "2px solid white",
        "position":"relative","right":"8%"}),
    
    html.Button("Bodyweight And Strength", style = {
        "background-color":"transparent",
        "color":"white",
        "border-radius": "7px",
        "cursor": "pointer",
        "padding":"12px 20px 12px 20px",
        "font-size":"14px",
        "border": "2px solid white",
        "position":"relative","left":"5%"}),

    html.Button("Age And Strength", style = {
        "background-color":"transparent",
        "color":"white",
        "border-radius": "7px",
        "cursor": "pointer",
        "padding":"12px 20px 12px 20px",
        "font-size":"14px",
        "border": "2px solid white",
        "position":"relative","left":"20%"})])

 # Visualization Space





], style = {"background-color":"#2E2E2E","color":"white","text-align":"center"}) # End of Outer Div





if (__name__ == '__main__'):
    app.run_server(debug= True)
