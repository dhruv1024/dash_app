# app_portfolio.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)
app.title = "Portfolio Optimization"
server = app.server

app.layout = html.Div([
    html.H1("Portfolio Optimization - Efficient Frontier"),
    html.P("Adjust expected return and risk assumptions."),
    
    html.Label("Expected Return (%)"),
    dcc.Slider(id='exp_return', min=5, max=20, step=0.5, value=10,
               marks={i: f"{i}%" for i in range(5,21,5)}),
    
    html.Label("Portfolio Std Dev (%)"),
    dcc.Slider(id='risk', min=5, max=30, step=0.5, value=15,
               marks={i: f"{i}%" for i in range(5,31,5)}),
    
    dcc.Graph(id='frontier_plot')
])

@app.callback(
    Output('frontier_plot', 'figure'),
    Input('exp_return', 'value'),
    Input('risk', 'value')
)
def update_frontier(exp_return, risk):
    # Simulated Efficient Frontier
    risks = np.linspace(5, 30, 100)
    returns = exp_return + 0.5 * (risks - risk)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=risks, y=returns, mode='lines+markers', name="Efficient Frontier"))
    fig.update_layout(title="Efficient Frontier", xaxis_title="Risk (Std Dev %)", yaxis_title="Expected Return (%)")
    return fig

if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run(debug=True)
    # Portfolio Optimization App (Efficient Frontier)
