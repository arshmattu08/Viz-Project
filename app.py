# imports
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, callback, State, dash

# Data 

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSv5T0GjnV3amAPzMDv2hsgAL1P_XeQBK_mlBzxwy9XAXvgo-J6_CBGKoC0_0St0L2aFldI8ztEvZgD/pub?output=csv"

df = pd.read_csv(url)

# Visualization Code

# Strength Distribution
box_fig = px.box(df, x = 'sex', y = 'best3bench_kg', color = 'sex', hover_data= 'age')

box_fig.update_layout(
    title = 'Distribution of upper body strength in men and women',
    template = 'simple_white',
    yaxis=dict(range=[0, df['best3bench_kg'].max()]),
    xaxis_title = 'Sex',
    yaxis_title = 'Bench Press in KG'
)


# Bodyweight and Strength

scatter_fig = px.scatter(df, x = 'bodyweight_kg', y = 'best3bench_kg')
scatter_fig.update_layout(
    template = 'simple_white',
    # xaxis=dict(range=[0, power_data['bodyweight_kg'].max()]),
    yaxis=dict(range=[0, df['best3bench_kg'].max()]),
    xaxis_title = 'Bodyweight in KG',
    yaxis_title = 'Benchpress in KG'

)

# Age and Strength

fig = px.scatter(df, x = "age", y = "best3bench_kg", color = 'sex') # default color map seems to work well

fig.update_layout(
    plot_bgcolor='white',
    xaxis=dict(range=[0, df['age'].max()]),
    yaxis=dict(range=[0, df['best3bench_kg'].max()]),
    title_text = 'Age vs bench press strength in men and women',
    xaxis_title = 'Age',
    yaxis_title = 'Bench Press in KG',
    legend_title = 'Sex')


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
        html.Button("View Dataset",id = "view_data", style={
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
        "backgroundColor": "#111e40",
        "height": "100vh",
        "position": "fixed",
        "top": 0,
        "left": 0,
    }),

# Visualization Toggle Buttons
html.Div([
    html.Button("Strength Distribution", id = "first-button",style = {
        "background-color":"transparent",
        "color":"white",
        "border-radius": "7px",
        "cursor": "pointer",
        "padding":"12px 20px 12px 20px",
        "font-size":"14px",
        "border": "2px solid white",
        "position":"relative","right":"8%"}),
    
    html.Button("Bodyweight And Strength", id = "second-button",style = {
        "background-color":"transparent",
        "color":"white",
        "border-radius": "7px",
        "cursor": "pointer",
        "padding":"12px 20px 12px 20px",
        "font-size":"14px",
        "border": "2px solid white",
        "position":"relative","left":"5%"}),

    html.Button("Age And Strength", id = "third-button",style = {
        "background-color":"transparent",
        "color":"white",
        "border-radius": "7px",
        "cursor": "pointer",
        "padding":"12px 20px 12px 20px",
        "font-size":"14px",
        "border": "2px solid white",
        "position":"relative","left":"20%"})]),

 # Visualization and Dataset Space
html.Div([
        dcc.Graph(id= "my-graph", style = {
            "width":"60%",
            "position":"relative","left":"28%",
            "margin-top":"59px",}),

        dcc.Markdown(id = "msg", style={"position":"relative","left":"100px","font-weight":'bold','color':'#6eb7ff'})
    ])

], style = {"background-color":"#2E2E2E","color":"white","text-align":"center"}) # End of Outer Div


# Callback Functionality

# Strength distribution
@callback(
    Output('my-graph','figure'),
    Output('msg','children'),
    Input('first-button','n_clicks'),
    prevent_initial_call='initial_duplicate')
def show_box(n):
    if n is not None and n > 0:
        msg = '''Men have an higher median in bench press compared to women. Overall variation in men seem much higher    
    as well in how much they lift.Both groups have several observations outside the IQR.
        '''
        return box_fig,msg
    return dash.no_update,""
    
# Bodyweight and Strength
@callback(
    Output('my-graph','figure',allow_duplicate=True),
    Output('msg','children', allow_duplicate=True),
    Input('second-button','n_clicks'),
    prevent_initial_call='initial_duplicate')
def show_scatter(n):
    if n is not None and n > 0:
        msg = '''Benchpress tends to go up as the bodyweight increases of lifters.
'''
        return scatter_fig,msg
    return dash.no_update,""


# Age and Strength
@callback(
    Output('my-graph','figure',allow_duplicate=True),
    Output('msg','children',allow_duplicate=True),
    Input('third-button','n_clicks'),
    prevent_initial_call='initial_duplicate')
def show_scatter2(n):
    if n is not None and n > 0:
        msg = '''Age seems to play a key role in how much weight is lifted on bench press. It can be seen that  
        after age of approx. 40, performance begins to decrease.'''
        return fig,msg
    return dash.no_update,""




if (__name__ == '__main__'):
    app.run(debug= True)
