# Bollinger Bands - short introduction

Bollinger Bands consist of :
- an N-period moving average (MA), 
- an upper band at K times an N-period standard deviation above the moving average (MA + Kσ), 
- and a lower band at K times an N-period standard deviation below the moving average (MA − Kσ).

Typical values for N and K are **20** days and **2**, respectively.


import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf


df = yf.download(tickers='BNP.PA', period = '1d', interval ='1m')

#Interval required 1 minute

df['Middle Band'] = df['Close'].rolling(window=20).mean() 
df['Lower Band'] = df['Middle Band'] - 2*df['Close'].rolling(window=20).std()
df['Upper Band'] = df['Middle Band'] + 2*df['Close'].rolling(window=20).std()

# declare figure

fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y = df['Middle Band'], line=dict(color='blue', width=.7),name = 'Middle Band'))
fig.add_trace(go.Scatter(x=df.index, y = df['Upper Band'], line=dict(color='red', width=1.5),name = 'Upper Band'))
fig.add_trace(go.Scatter(x=df.index, y = df['Lower Band'], line=dict(color='green', width=1.5),name = 'Lower Band'))

# Candlestick
fig.add_trace(go.Candlestick(x=df.index,
                             open = df['Open'],
                             high = df['High'],
                             low = df['Low'],
                             close = df['Close'], name = 'Market Data'))

# Add titles
fig.update_layout(
    title = 'BNP live share price evolution',
    yaxis_title = 'Stock Price (EUR per Share)')


# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=15,
                     label="15m",
                     step="minute",
                     stepmode="backward"),
                dict(count=45,
                     label="45m",
                     step="minute",
                     stepmode="backward"),
                dict(count=1,
                     label="HTD",
                     step="hour",
                     stepmode="todate"),
                dict(count=3,
                     label="3h",
                     step="hour",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

# Show Figure
fig.show()


