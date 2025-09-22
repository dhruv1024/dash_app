# app_portfolio_dashboard.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Financial Portfolio Dashboard"
server = app.server

# --- DCF Data ---
years = [1,2,3,4,5]
default_cashflows = [100,120,140,160,180]

# --- Portfolio Optimization Data ---
np.random.seed(42)
n_assets = 4
mean_returns = np.array([0.08,0.12,0.10,0.07])
cov_matrix = np.array([[0.10,0.02,0.04,0.00],
                       [0.02,0.08,0.01,0.00],
                       [0.04,0.01,0.09,0.02],
                       [0.00,0.00,0.02,0.05]])

# --- Scenario Analysis Data ---
scenarios = ["Base","Optimistic","Pessimistic"]
drivers = ["Revenue Growth","Cost Growth","CapEx"]
data = pd.DataFrame(np.random.rand(len(drivers), len(scenarios))*10, index=drivers, columns=scenarios)

# --- App Layout ---
app.layout = html.Div([
    html.H1("📊 Financial Analytics Dashboard", style={'textAlign':'center'}),
    
    dcc.Tabs(id="tabs", value='tab_dcf', children=[
        dcc.Tab(label="DCF Model", value='tab_dcf'),
        dcc.Tab(label="Portfolio Optimization", value='tab_portfolio'),
        dcc.Tab(label="Scenario Analysis", value='tab_scenario'),
    ]),
    
    html.Div(id='tabs_content')
])

# --- Tabs Callback ---
@app.callback(
    Output('tabs_content','children'),
    Input('tabs','value')
)
def render_tab(tab):
    if tab == 'tab_dcf':
        return html.Div([
            html.H2("Discounted Cash Flow (DCF) Model"),
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
    
    elif tab == 'tab_portfolio':
        return html.Div([
            html.H2("Portfolio Optimization - Efficient Frontier"),
            html.Label("Number of Portfolios"),
            dcc.Slider(id='n_portfolios', min=100, max=5000, step=100, value=500,
                       marks={i:str(i) for i in range(100,5001,1000)}),
            dcc.Graph(id='frontier_plot'),
            html.H3(id='sharpe_info')
        ])
    
    elif tab == 'tab_scenario':
        return html.Div([
            html.H2("Scenario & Sensitivity Analysis"),
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
            
            html.Label("Select Scenario"),
            dcc.Dropdown(id='scenario_dropdown', options=[{"label":s,"value":s} for s in scenarios],
                         value="Base"),
            dcc.Graph(id='heatmap')
        ])

# --- DCF Callbacks ---
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
    
    if terminal_method=="gordon":
        terminal_value = default_cashflows[-1]*(1+growth_rate)/(discount-growth_rate)
    else:
        terminal_value = default_cashflows[-1]*10
    
    discounted_terminal = terminal_value / ((1+discount)**years[-1])
    total_valuation = sum(discounted) + discounted_terminal
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"Year {y}" for y in years], y=discounted, name="Discounted Cashflows"))
    fig.add_trace(go.Bar(x=["Terminal Value"], y=[discounted_terminal], name="Terminal Value"))
    fig.update_layout(title="DCF Valuation", barmode='group', yaxis_title="Value ($)")
    
    return fig, f"Total Enterprise Value: ${total_valuation:,.2f}"

# --- Portfolio Callbacks ---
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

# --- Scenario Callbacks ---
@app.callback(
    Output('heatmap','figure'),
    Input('scenario_dropdown','value'),
    Input({'type':'driver_slider','index':dash.dependencies.ALL}, 'value')
)
def update_heatmap(selected_scenario, slider_values):
    temp_data = data.copy()
    temp_data[selected_scenario] = slider_values
    fig = px.imshow(temp_data.T, text_auto=True, labels=dict(x="Drivers", y="Scenario", color="Impact"),
                    color_continuous_scale='RdBu_r')
    return fig

# --- Run App ---
if __name__=="__main__":
    app.run(debug=True)
