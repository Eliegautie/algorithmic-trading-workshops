from profitview import Link, http, logger

import numpy as np
from numpy import array
import pandas as pd
import scipy
import talib


class Trading(Link):
	def __init__(self):		
        super().__init__()
        self.closes = []
		self.src = 'bitmex' # exchange name
        self.venue = 'BitMEX' # API key name
        self.sym = 'XBTUSD'  # symbol we will trade
        self.level = '1m' # OHLC candle granularity
		
		
	def on_startup(self):
		self.fetch_latest_closes()
		self.fetch_current_risk()		
		
	def fetch_current_risk(self):
		orders = self.fetch_open_orders('BitMEX')
		positions = self.fetch_positions('BitMEX')
		
	def quote_update(self, src, sym, data):
		if sym == self.sym:
			self.best_bid = data['bid'][0]
			self.best_ask = data['ask'][0]	
	
		 
    def trade_update(self, src, sym, data):		
        """Event: receive market trades from subscribed symbols"""
		candles = self.fetch_candles(self.venue, sym=self.sym, level=self.level)['data']
        self.closes = [x['close'] for x in candles]
		closes = array(self.closes)
		
		RSI = talib.RSI(closes)	
			
		if RSI[-1] > 75:      
			self.create_limit_order(self.venue, sym=self.sym, side="Sell", size=100, price=self.best_ask)
			
		if RSI[-1] < 25:
			self.create_limit_order(self.venue, sym=self.sym, side="Buy", size=100, price=self.best_bid)
