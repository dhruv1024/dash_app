# app_scenario.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
app.title = "Scenario Analysis"
server = app.server

# Sample data
scenarios = ["Base", "Optimistic", "Pessimistic"]
drivers = ["Revenue Growth", "Cost Growth", "CapEx"]
data = pd.DataFrame(np.random.rand(len(drivers), len(scenarios))*10, index=drivers, columns=scenarios)

app.layout = html.Div([
    html.H1("Scenario & Sensitivity Analysis"),
    html.P("Select scenario to see impact on key drivers."),
    
    dcc.Dropdown(id='scenario_dropdown', options=[{"label": s, "value": s} for s in scenarios],
                 value="Base"),
    
    dcc.Graph(id='heatmap')
])

@app.callback(
    Output('heatmap', 'figure'),
    Input('scenario_dropdown', 'value')
)
def update_heatmap(selected_scenario):
    fig = px.bar(x=drivers, y=data[selected_scenario], labels={'x':'Driver','y':'Impact'}, 
                 title=f"Scenario: {selected_scenario}")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
    # Scenario & Sensitivity Analysis App
