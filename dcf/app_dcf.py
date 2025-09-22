# app_dcf_enhanced.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
app.title = "Enhanced DCF Dashboard"
server = app.server

# Default cashflows for 5 years
years = [1,2,3,4,5]
default_cashflows = [100,120,140,160,180]

app.layout = html.Div([
    html.H1("Discounted Cash Flow (DCF) Model"),
    html.P("Adjust assumptions to see changes in valuation."),
    
    html.Label("Discount Rate (%)"),
    dcc.Slider(id='discount_rate', min=5, max=20, step=0.5, value=10,
               marks={i: f"{i}%" for i in range(5,21,5)}),
    
    html.Label("Select Growth Scenario"),
    dcc.Dropdown(id='growth_scenario',
                 options=[{"label":"Base", "value":0.03},
                          {"label":"Optimistic", "value":0.05},
                          {"label":"Pessimistic", "value":0.01}],
                 value=0.03),
    
    html.Label("Terminal Value Method"),
    dcc.RadioItems(id='terminal_method',
                   options=[{"label":"Gordon Growth", "value":"gordon"},
                            {"label":"Exit Multiple", "value":"multiple"}],
                   value="gordon"),
    
    dcc.Graph(id='dcf_plot'),
    html.H3(id='total_value')
])

@app.callback(
    Output('dcf_plot','figure'),
    Output('total_value','children'),
    Input('discount_rate','value'),
    Input('growth_scenario','value'),
    Input('terminal_method','value')
)
def update_dcf(discount_rate, growth_rate, terminal_method):
    discount = discount_rate/100
    discounted = [cf / ((1+discount)**year) for cf, year in zip(default_cashflows, years)]
    
    # Terminal Value
    if terminal_method=="gordon":
        terminal_value = default_cashflows[-1]*(1+growth_rate)/(discount-growth_rate)
    else:
        terminal_value = default_cashflows[-1]*10  # Simple exit multiple
    
    discounted_terminal = terminal_value / ((1+discount)**years[-1])
    total_valuation = sum(discounted) + discounted_terminal
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"Year {y}" for y in years], y=discounted, name="Discounted Cashflows"))
    fig.add_trace(go.Bar(x=["Terminal Value"], y=[discounted_terminal], name="Terminal Value"))
    fig.update_layout(title="DCF Valuation", barmode='group', yaxis_title="Value ($)")
    
    return fig, f"Total Enterprise Value: ${total_valuation:,.2f}"

if __name__=="__main__":
    app.run(debug=True)
