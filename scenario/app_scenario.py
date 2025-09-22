# app_scenario_enhanced.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
app.title = "Enhanced Scenario Analysis"
server = app.server

scenarios = ["Base","Optimistic","Pessimistic"]
drivers = ["Revenue Growth","Cost Growth","CapEx"]

# Base data
data = pd.DataFrame(np.random.rand(len(drivers), len(scenarios))*10, index=drivers, columns=scenarios)

app.layout = html.Div([
    html.H1("Scenario & Sensitivity Analysis"),
    html.P("Adjust driver values to see impact on scenario."),
    
    html.Div([
        html.Div([
            html.Label(driver),
            dcc.Slider(
                id={'type':'driver_slider','index':driver},
                min=0, max=20, step=0.5, value=data.loc[driver,"Base"],
                marks={i:str(i) for i in range(0,21,5)}
            )
        ]) for driver in drivers
    ]),
    
    dcc.Dropdown(id='scenario_dropdown', options=[{"label":s,"value":s} for s in scenarios],
                 value="Base"),
    
    dcc.Graph(id='heatmap')
])

@app.callback(
    Output('heatmap','figure'),
    Input('scenario_dropdown','value'),
    Input({'type':'driver_slider','index':dash.dependencies.ALL}, 'value')
)
def update_heatmap(selected_scenario, slider_values):
    temp_data = data.copy()
    temp_data[selected_scenario] = slider_values
    fig = px.imshow(temp_data.T, text_auto=True, labels=dict(x="Drivers", y="Scenario", color="Impact"))
    return fig

if __name__=="__main__":
    app.run(debug=True)
