import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

# Sample data generation function
def generate_data():
    return pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', periods=100),
        'Portfolio Value': [10000 + i * 100 for i in range(100)],
        'Trade Volume': [100 + i * 10 for i in range(100)]
    })

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Algorithmic Trading Dashboard"),
    dcc.Interval(
        id='interval-component',
        interval=1*60000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Graph(id='portfolio-value-chart'),
    html.Div(id='portfolio-value-summary', style={'padding': 10}),
    dcc.Graph(id='trade-volume-chart'),
    html.Div(id='trade-volume-summary', style={'padding': 10})
])

# Callback to update data
@app.callback(
    [Output('portfolio-value-chart', 'figure'),
     Output('portfolio-value-summary', 'children'),
     Output('trade-volume-chart', 'figure'),
     Output('trade-volume-summary', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_charts(n):
    df = generate_data()
    portfolio_fig = px.line(df, x='Date', y='Portfolio Value', title='Portfolio Value Over Time')
    trade_volume_fig = px.bar(df, x='Date', y='Trade Volume', title='Trade Volume Over Time')
    summary_text_portfolio = "Updated portfolio value over time."
    summary_text_trade_volume = "Updated trade volume over time."
    return portfolio_fig, summary_text_portfolio, trade_volume_fig, summary_text_trade_volume

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
