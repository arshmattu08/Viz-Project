# imports
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import Dash, html, dcc, Input, Output, callback, State, dash, dash_table, callback_context, exceptions

# Data 
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSv5T0GjnV3amAPzMDv2hsgAL1P_XeQBK_mlBzxwy9XAXvgo-J6_CBGKoC0_0St0L2aFldI8ztEvZgD/pub?output=csv"

#fixing date column
df = pd.read_csv(url)
df['date'] = pd.to_datetime(df['date'], format= "%m/%d/%y").dt.date

# when viewing data, make sure no NA values show up
df_cleaned = df.dropna()
df_sampled = df_cleaned.sample(n=10)


# App code
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
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

        html.H2("Filter", style = {
            "color":"white",
            "position":"relative","top":"140px",
            "font-size":"39px",
            "font-family":"Roboto, sans-serif"}),

         dcc.Dropdown(id = "gender-dropdown",options=[
             {'label':'Male','value':'M'},
             {'label':'Female','value':'F'}
         ], placeholder="Gender", value = 'M',style = {
            "position":"relative","top":"75px","left":"12px",
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

        dcc.Markdown(id = "msg", style={"position":"relative","left":"100px","font-weight":'bold','color':'#6eb7ff'}),

        html.Div(id='data-table-container', style= {'display': 'none', 'padding': '30px', 'width': '80%', 'margin': 'auto'}),

        dcc.Store(id="active-graph")
    ])

], style = {"background-color":"#2E2E2E","color":"white","text-align":"center"}) # End of Outer Div


# Callback Functionality

# Strength distribution
@callback(
    Output('my-graph','figure'),
    Output('msg','children'),
    Input('gender-dropdown','value'),
    Input('active-graph','data'),
    prevent_initial_call= True)
def show_box(drop_value,active_graph):
    df_filtered = df.loc[df['sex'] == drop_value,:]
    box_fig = px.box(df_filtered, x = 'sex', y = 'best3bench_kg', color = 'sex', hover_data= 'age')

    if active_graph == 'first-button':
        box_fig.update_layout(
        title = 'Distribution of upper body strength in men and women',
        template = 'simple_white',
        yaxis=dict(range=[0, df['best3bench_kg'].max()]),
        xaxis_title = 'Sex',
        yaxis_title = 'Bench Press in KG')

        box_fig.add_annotation(
        x= 0.32,
        y= 210,
        text="Compare the variation in two groups <br> using filter",
        showarrow=True,
        arrowhead=2,
        arrowwidth=1.5,
        ax=75, ay= -30,
        font=dict(size=13, color="black", weight = 'bold') )

        
        msg = '''Men have an higher median in bench press compared to women. Overall variation in men seem much higher    
        as well in how much they lift.Both groups have several observations outside the IQR.
            '''
        return box_fig,msg
    return dash.no_update,""
    
# Bodyweight and Strength
@callback(
    Output('my-graph','figure',allow_duplicate=True),
    Output('msg','children', allow_duplicate=True),
    Input('gender-dropdown','value'),
    Input('active-graph','data'),
    prevent_initial_call=True)
def show_scatter(drop_value,active_graph):
    df_filtered = df.loc[df['sex'] == drop_value,:]

    if active_graph == 'second-button':
        scatter_fig = px.scatter(df_filtered, x = 'bodyweight_kg', y = 'best3bench_kg',color ='sex')
        scatter_fig.update_layout(
        template = 'simple_white',
        # xaxis=dict(range=[0, power_data['bodyweight_kg'].max()]),
        yaxis=dict(range=[0, df['best3bench_kg'].max()]),
        xaxis_title = 'Bodyweight in KG',
        yaxis_title = 'Benchpress in KG')

        scatter_fig.add_annotation(
        x= 90,
        y= 360,
        text="Clear rising trend in bodyweight and bench",
        showarrow=True,
        arrowhead=2,
        arrowwidth=1.5,
        ax=-60, ay= -30,
        font=dict(size=11, color="black", weight = 'bold'))

        
        msg = '''Benchpress tends to go up as the bodyweight increases of lifters.
            '''
        return scatter_fig,msg
    return dash.no_update,""


# Age and Strength
@callback(
    Output('my-graph','figure',allow_duplicate=True),
    Output('msg','children', allow_duplicate=True),
    Input('gender-dropdown','value'),
    Input('active-graph','data'),
    Input('third-button','n_clicks'),
    prevent_initial_call= True)
def show_scatter2(drop_value,active_graph,n):
    df_filtered = df.loc[df['sex'] == drop_value,:]

    if active_graph == 'third-button':
        fig = px.scatter(df_filtered, x = "age", y = "best3bench_kg", color = 'sex') 

        fig.update_layout(
            plot_bgcolor='white',
            xaxis=dict(range=[0, df['age'].max()]),
            yaxis=dict(range=[0, df['best3bench_kg'].max()]),
            title_text = 'Age vs bench press strength in men and women',
            xaxis_title = 'Age',
            yaxis_title = 'Bench Press in KG',
            legend_title = 'Sex')


        fig.add_annotation(
            x= 55,
            y= 340,
            text="Performance begins to decrease",
            showarrow=True,
            arrowhead=2,
            arrowwidth=1.5,
            ax=60, ay= -30,
            font=dict(size=11, color="black", weight = 'bold'))

        msg = '''Age seems to play a key role in how much weight is lifted on bench press. It can be seen that  
            after age of approx. 40, performance begins to decrease.'''
        return fig,msg
    return dash.no_update,""


# Dataset Display
@callback(
    Output('data-table-container', 'children'),
    Output('data-table-container', 'style'),
    Input('view_data', 'n_clicks'),
    prevent_initial_call=True)
def display_table(n):
    if n and n%2 != 0: # allow toggling
        table = dash_table.DataTable(
            data=df_sampled.to_dict('records'),
            columns=[{"name": str(col), "id": str(col)} for col in df_sampled.columns],
            page_size=10,
            style_table={'overflowX': 'auto',"width":"60%","color":"blue","position":"relative","left":"403px",
                         "margin-top":"30px","margin-bottom":"40px"},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
        )
        return table, {'display': 'block'}
    return dash.no_update, {'display': 'none'}

# Storing last button clicked data, this will help in filters.
@callback(
    Output('active-graph', 'data'),
    Input('first-button', 'n_clicks'),
    Input('second-button', 'n_clicks'),
    Input('third-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_active_graph(n1, n2, n3):
    ctx = callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id




if (__name__ == '__main__'):
    app.run(debug= True)



