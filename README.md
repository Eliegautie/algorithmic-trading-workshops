## Algorithmic trading courses

- For almost a year, I have been working on developing my coding and data analysis skills in close collaboration with the two founders of Profitview Richard Hickling and Jahan Zahid (https://profitview.net/). After several months of training, taking courses on Codecademy, testing my skills on Codility, and building the premise of a Bitcoin trading algo (working with Jahan), I now have a decent level of programming.


- Since March, Profitview has launched a series of webinars in which participants, supervised by Jahan, backtest and deploy an algorithmic trading strategy in a live environment. These webinars are the beginnings of an algorithmic trading course that should start soon, where we will work on building an effective algorithmic trading program. You can find the work done so far in these webinars here: https://github.com/profitviews/workshops. 


- In addition to taking these courses, I also subscribed to the algorithmic trading platform Profitview (Hobbyist), which allows me to get live data from different exchanges and build my algorithm more easily. You can see the basics of the ProfitView Trading Bots tab here: 
https://profitview.net/docs/trading/?utm_source=convertkit&utm_medium=email&utm_campaign=Workshop+Replay%3A+Algorithmic+Trading+with+Python+part+2%20-%2010531534

- In this repository, my goal is to develop and backtest trading strategies, which I could then propose during workshops before implementing them in a real environment with ProfitView Trading bot.


## Trading Strategies:  

*RSI* 

-This strategy is based on the Relative Strength Indicator (RSI). This indicator allows to know 2 things: the power of a trend and indicates if the market is overbought or oversold.

The classic RSi formula is as follows: RSI= 100 - [100/(1+ up_ewm/down_ewm)]

With : 

H which is the average of the increases over the last X Units of Time.

B which is the average of the decreases during the X last X Units of Time.

RSI > 70: it means that the market is probably overbought.
RSI < 30: it means that the market is probably oversold


- First, we need to get an idea of how often the RSI occurs with a value above 70 or below 30 in our time series. To do this, we compute the RSI with Talib and plot the frequency of the different RSI levels in 100 bins (**Fig.1**). We can see that the histogram is bell-shaped and that values above 70 or below 30 are less dominant.

- I then plot the closing price and RSI values (over a 13-hour period) on the same chart to see if when the RSI > 70, prices fall or when the RSI < 30, prices rise (**Fig.2**).
From this chart, I can assume that the strategy should produce interesting results.

- Trading idea: I want to know, given the current closing prices, what the "hypothetical" RSI would be if the price rose by 2% (**Fig.3**).
To do this, we use the hypo_rsi function. The reason for this function in this algo is that I can use it to set limit orders when the RSI is at any level. To do this, I need to solve the inverse equation: what return do I need to get a given ROI?

- This is exactly what I did next. First, I calculated the RSI manually with the exponential weighted moving average and got the same results as with Talib. Then, given the current RSI, the current average of the increases over the last 14 minutes (up_ewm) and the current average of the decreases over the last 14 minutes (down_ewm), what would be the "hypothetical" returns if the RSI were to increase by 1 point for example




