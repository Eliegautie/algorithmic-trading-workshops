rom profitview import Link, logger
import talib
import numpy as np


   
class Trading(Link):
    
    def __init__(self):
        super().__init__()
        # ALGO PARAMS
        self.src = 'bitmex' # exchange name
        self.venue = 'BitMEX' # API key name
        self.sym = 'XBTUSD'  # symbol we will trade
        self.level = '1m' # OHLC candle granularity
        self.lookback = 14 # number of close prices 
        self.time_step = TIME_LOOKUP[self.level] # time step in milliseconds
        
        # ALGO STRATEGY STATE
        self.last = None # last price update
        self.closes = dict() # time bin -> close price    
        
        # RUN ON STARTUP
        self.on_startup()

 
