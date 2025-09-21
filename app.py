import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

# Read data from Excel, skipping the first rows with metadata
df = pd.read_excel("historicalweeklydata.xlsx", skiprows=7)  # Adjust skiprows as needed

# Rename columns for clarity (adjust based on your actual data)
df = df.rename(columns={
    df.columns[0]: "Week",
    df.columns[1]: "30yr Rate",
    df.columns[2]: "15yr Rate",
    df.columns[3]: "5/1 ARM Rate"
})

print("Excel columns after rename:", df.columns)  # Debug

# Use 'Week' as the date column
date_col = "Week"
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

app = dash.Dash(__name__)
server = app.server # Expose the server variable for deployments

app.layout = html.Div([
    html.H1("Freddie Mac PMMS: Weekly Mortgage Rates"),

    # 30-Year Fixed Rate Trend
    dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=df[date_col],
                    y=df["30yr Rate"],
                    mode='lines+markers',
                    name='30yr FRM Rate'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Interest Rate (%)'},
                title='30-Year Fixed Mortgage Rate Over Time'
            )
        }
    ),

    # 15-Year Fixed Rate Trend
    dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=df[date_col],
                    y=df["15yr Rate"],
                    mode='lines+markers',
                    name='15yr FRM Rate',
                    line=dict(color='orange')
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Interest Rate (%)'},
                title='15-Year Fixed Mortgage Rate Over Time'
            )
        }
    ),

    # 5/1 ARM Rate Trend
    dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=df[date_col],
                    y=df["5/1 ARM Rate"],
                    mode='lines+markers',
                    name='5/1 ARM Rate',
                    line=dict(color='green')
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Interest Rate (%)'},
                title='5/1 ARM Mortgage Rate Over Time'
            )
        }
    ),

    # Comparison Chart
    dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=df[date_col],
                    y=df["30yr Rate"],
                    mode='lines',
                    name='30yr FRM Rate'
                ),
                go.Scatter(
                    x=df[date_col],
                    y=df["15yr Rate"],
                    mode='lines',
                    name='15yr FRM Rate'
                ),
                go.Scatter(
                    x=df[date_col],
                    y=df["5/1 ARM Rate"],
                    mode='lines',
                    name='5/1 ARM Rate'
                ),
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Interest Rate (%)'},
                title='Mortgage Rate Comparison'
            )
        }
    ),
])

if __name__ == '__main__':
    app.run(debug=True)