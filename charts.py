import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_stock_price(df, symbol):
    """
    Creates an interactive line chart for stock closing price.
    """
    fig = px.line(df, x='Date', y='Close', title=f'{symbol} Stock Price History')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price (INR)',
        template='plotly_dark',
        hovermode='x unified'
    )
    return fig

def plot_candlestick(df, symbol):
    """
    Creates a candlestick chart for the stock.
    """
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    fig.update_layout(
        title=f'{symbol} Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price (INR)',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    return fig

def plot_volume(df, symbol):
    """
    Creates a bar chart for trading volume.
    """
    fig = px.bar(df, x='Date', y='Volume', title=f'{symbol} Trading Volume')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Volume',
        template='plotly_dark'
    )
    return fig

def plot_industry_pie(df):
    """
    Creates a pie chart showing market share by industry (based on Volume).
    """
    # Group by Industry and sum Volume
    industry_vol = df.groupby('Industry')['Volume'].sum().reset_index()
    
    fig = px.pie(industry_vol, values='Volume', names='Industry', title='Market Share by Industry (Volume)')
    fig.update_layout(template='plotly_dark')
    return fig

def plot_industry_comparison(df):
    """
    Creates a bar chart comparing average closing price across industries.
    """
    industry_avg = df.groupby('Industry')['Close'].mean().reset_index().sort_values('Close', ascending=False)
    
    fig = px.bar(industry_avg, x='Industry', y='Close', title='Average Stock Price by Industry')
    fig.update_layout(
        xaxis_title='Industry',
        yaxis_title='Avg Price (INR)',
        template='plotly_dark',
        xaxis_tickangle=-45
    )
    return fig
