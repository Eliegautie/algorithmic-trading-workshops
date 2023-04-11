import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf


df = yf.download(tickers='BNP.PA', period = '1d', interval ='1m')

# Interval required 1 minute

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



# Creating the Trading Strategy

def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0
    
    for i in range(1,len(df)):
        if df['Close'][i-1] > df['Lower Band'][i-1] and df['Close'][i] < df['Lower Band'][i]:
            if signal != 1:
                buy_price.append(df['Close'][i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append(signal)
                
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
                
        elif df['Close'][i-1] < df['Upper Band'][i-1] and df['Close'][i] > df['Upper Band'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(df['Close'][i])
                signal = -1
                bb_signal.append(signal)
                
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
                
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)
            
    return buy_price, sell_price, bb_signal

buy_price, sell_price, bb_signal = implement_bb_strategy(df['Close'], df['Lower Band'], df['Upper Band'])

# Plotting the Trading lists

df['Close'].plot(label = 'Close Prices', alpha = 0.3)
df['Upper Band'].plot(label = 'Upper Band', linestyle = '--', linewidth = 1, color = 'red')
df['Middle Band'].plot(label = 'Middle Band', linestyle = '--', linewidth = 1.2, color = 'blue')
df['Lower Band'].plot(label = 'Lower Band', linestyle = '--', linewidth = 1, color = 'green')
plt.scatter(df.index[:-1], buy_price, marker = '^', color = 'green', label = 'Buy', s = 100)
plt.scatter(df.index[:-1], sell_price, marker = 'v', color = 'red', label = 'Sell', s = 100)
plt.title('BNP Bollinger Band Strategy Trading Signals')
plt.legend(loc = 'upper right')
plt.ylabel('Price', fontsize=12)
plt.xlabel('time', fontsize=12)
plt.show()
