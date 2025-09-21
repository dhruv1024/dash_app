# app_dcf.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Sample DCF assumptions
base_cashflows = [100, 120, 140, 160, 180]  # Year 1-5
terminal_growth = 0.03

app = dash.Dash(__name__)
app.title = "DCF Dashboard"
server = app.server

app.layout = html.Div([
    html.H1("Discounted Cash Flow (DCF) Model"),
    html.P("Adjust assumptions to see changes in valuation."),
    
    html.Label("Discount Rate (%)"),
    dcc.Slider(id='discount_rate', min=5, max=20, step=0.5, value=10,
               marks={i: f"{i}%" for i in range(5,21,5)}),
    
    html.Label("Terminal Growth Rate (%)"),
    dcc.Slider(id='growth_rate', min=0, max=10, step=0.1, value=3,
               marks={i: f"{i}%" for i in range(0,11,2)}),
    
    dcc.Graph(id='dcf_plot')
])

@app.callback(
    Output('dcf_plot', 'figure'),
    Input('discount_rate', 'value'),
    Input('growth_rate', 'value')
)
def update_dcf(discount_rate, growth_rate):
    discount = discount_rate / 100
    terminal = growth_rate / 100
    years = list(range(1, 6))
    discounted = [cf / ((1+discount)**year) for cf, year in zip(base_cashflows, years)]
    terminal_value = base_cashflows[-1] * (1 + terminal) / (discount - terminal)
    discounted_terminal = terminal_value / ((1 + discount) ** 5)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"Year {y}" for y in years], y=discounted, name="Discounted Cashflows"))
    fig.add_trace(go.Bar(x=["Terminal Value"], y=[discounted_terminal], name="Terminal Value"))
    fig.update_layout(title="DCF Valuation", barmode='group', yaxis_title="Value ($)")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
    # Discounted Cash Flow (DCF) Model
