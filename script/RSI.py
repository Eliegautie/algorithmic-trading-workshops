#In progress ...

from profitview import Link, http, logger


import numpy as np
import pandas as pd
import talib
import threading
import time
  

TIME_LOOKUP = {
    '1m':  60_000,
    '15m': 60_000 * 15,
    '1h':  60_000 * 60,
    '1d':  60_000 * 60 * 24,    
}


class Trading(Link):
    
    def __init__(self):
        super().__init__()
        # ALGO PARAMS
        self.src = 'bitmex'                          # exchange name
        self.venue = 'BitMEX'                        # API key name
        self.sym = 'XBTUSD'                          # symbol we will trade
        self.level = '1m'                            # OHLC candle granularity
        self.lookback = 150                          # lookback period of close prices 
        self.time_step = TIME_LOOKUP[self.level]     # time step in milliseconds
        
        # ALGO STRATEGY STATE
        self.closes = dict()                          # time bin -> close price
        self.rsi = dict(rsi=np.nan)                   # MACD histogram and slope value
        self.risk = 0                                 # current position risk for sym
        self.orders = dict(bid={}, ask={})            # current open limit orders
        
        # ALGO PARAMS        
        
        # RUN ON STARTUP
        self.on_startup()

    @property
    def time_bin_now(self):
        return self.candle_bin(self.epoch_now, self.level)
    
    # MARKET DATA STATE     
    def on_startup(self):
        self.fetch_latest_closes()
        self.fetch_current_risk()
        
        

    def fetch_latest_closes(self):
        for x in self.fetch_candles(self.venue, sym=self.sym, level=self.level)['data']:
            if x['time'] not in self.closes:
                self.closes[x['time']] = x['close']
        
    def fetch_current_risk(self):
        for x in self.fetch_open_orders(self.venue)['data']:
            if x['sym'] == self.sym:
                key = 'bid' if x['side'] == 'Buy' else 'ask'
                self.orders[key][x['order_id']] = x
                
        for x in self.fetch_positions(self.venue)['data']:
            if x['sym'] == self.sym:
                sign = 1 if x['side'] == 'Buy' else -1
                self.risk = sign * x['pos_size']
            
      
     
    @property
    def last_closes(self):
        start_time = self.time_bin_now - self.lookback * self.time_step
        times = [start_time + (i + 1) * self.time_step for i in range(self.lookback)] 
        closes = [self.closes.get(x, np.nan) for x in times]
        return np.array(pd.Series(closes).ffill())
    
    def update_signal(self):
        closes = self.last_closes 
        if not any(np.isnan(closes)):        
            rsi = talib.RSI(self.last_closes) 
			self.rsi['rsi'] = rsi[-1]
			logger.info((self.rsi))
          
            
    def update_close(self, data):
        time_bin = self.candle_bin(data['time'], self.level)
        self.closes[time_bin] = data['price']   
		
	def trade_update(self, src, sym, data):
        if sym == self.sym:
            self.update_close(data)
            self.update_signal()
 	
