# app_portfolio_enhanced.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

np.random.seed(42)
app = dash.Dash(__name__)
app.title = "Enhanced Portfolio Optimization"
server = app.server

# Sample asset data
n_assets = 4
mean_returns = np.array([0.08,0.12,0.10,0.07])
cov_matrix = np.array([[0.10,0.02,0.04,0.00],
                       [0.02,0.08,0.01,0.00],
                       [0.04,0.01,0.09,0.02],
                       [0.00,0.00,0.02,0.05]])

app.layout = html.Div([
    html.H1("Portfolio Optimization - Efficient Frontier"),
    
    html.Label("Number of Portfolios"),
    dcc.Slider(id='n_portfolios', min=100, max=5000, step=100, value=500,
               marks={i:str(i) for i in range(100,5001,1000)}),
    
    dcc.Graph(id='frontier_plot'),
    html.H3(id='sharpe_info')
])

@app.callback(
    Output('frontier_plot','figure'),
    Output('sharpe_info','children'),
    Input('n_portfolios','value')
)
def update_frontier(n_portfolios):
    results = np.zeros((3,n_portfolios))
    weights_record = []

    for i in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        port_return = np.sum(weights*mean_returns)
        port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = port_return / port_std
        results[:,i] = [port_return, port_std, sharpe]
    
    # Optimal portfolio
    max_sharpe_idx = np.argmax(results[2])
    opt_return, opt_std, opt_sharpe = results[:,max_sharpe_idx]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=results[1], y=results[0], mode='markers',
                             marker=dict(color=results[2], colorscale='Viridis', showscale=True),
                             name="Portfolios", text=[f"Weights: {w.round(2)}" for w in weights_record]))
    fig.add_trace(go.Scatter(x=[opt_std], y=[opt_return], mode='markers', 
                             marker=dict(color='red', size=15), name="Max Sharpe"))
    fig.update_layout(title="Efficient Frontier", xaxis_title="Risk (Std Dev)", yaxis_title="Expected Return")
    
    return fig, f"Max Sharpe Portfolio: Return={opt_return:.2%}, Risk={opt_std:.2%}, Sharpe={opt_sharpe:.2f}"

if __name__=="__main__":
    app.run(debug=True)
