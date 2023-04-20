import time
import threading
from talib import EMA

from profitview import Bot, http, logger


class Trading(Bot):
    """read documentation"""

    def __init__(self):
        super().__init__()
        self.last_update = self.epoch_now
        self.risk = dict(Buy=0, Sell=0)
        self.get_risk()
        self.signal = 0 # float between -5 and 5
        thread = threading.Thread(target=self.update_orders)
        thread.start()

    def get_risk(self):
        api = self.apis['BitMEX']
        positions = api.get_positions()
        # [
        #     {'venue': '7f7e0f1d-aa8d-4f95-80f0-2258834534a5', 
        #     'sym': 'XBTUSD', 
        #     'side': 'Sell', 
        #     'size': 100.0, 
        #     'entry_price': 17993.0, 
        #     'liquidation_price': 100000000.0}
        # ]

        for x in positions:
            self.risk[x['side']] = x['size']

        logger.info(self.risk)

    def update_orders(self):
        src = 'bitmex'      
        sym = 'XBTUSD'
        risk_limit = 500
        api = self.apis['BitMEX']

        if market := self.quotes[src].get(sym):
            bid, bsize = market['bid']
            ask, asize = market['ask']
            spread = 5
            adj_bid = bid + self.signal - spread
            adj_ask = ask + self.signal + spread

            api.cancel_order()
            if self.risk['Buy'] <= 400:
                api.create_limit_order(sym, 'Buy', 100, adj_bid)
            if self.risk['Sell'] <= 400:
                api.create_limit_order(sym, 'Sell', 100, adj_ask)

        time.sleep(2)
        self.update_orders()

    def private_order(self, src, sym, data):
        """define order update logic"""
        logger.info(f'{src} {sym} {data}')

    def private_fill(self, src, sym, data):
        """define fill update logic"""
        # {
        #     'venue': '7f7e0f1d-aa8d-4f95-80f0-2258834534a5', 
        #     'id': '311962f0-5753-46c0-1bdc-4fc45341dd60', 
        #     'type': 'Market', 
        #     'side': 'Sell', 
        #     'price': 18024.5, 
        #     'size': 100.0,
        #     'time': 1671030243498
        # }
        self.risk[data['side']] += data['size']
        netted_amount = min(self.risk['Buy'], self.risk['Sell'])
        self.risk['Buy'] -= netted_amount
        self.risk['Sell'] -= netted_amount
        logger.info(self.risk)

    def public_quote(self, src, sym, data):
        """define quote update logic"""
        # logger.info(f'{src} {sym} {data}')
        # quote = data | {'src': src, 'sym': sym}
        # self.publish('quotes', quote)

    def public_trade(self, src, sym, data):
        """define trade update logic"""
        # create_limit_order(self, sym, side, size, price)
        # logger.info(f'{src} {sym} {data}')

    @http.route
    def post_mid(self, data):
        self.signal = float(data['signal'])

    @http.route
    def get_balances(self, data):
        api = self.apis[data['venue']]
        return api.get_balances()

    @http.route
    def get_quotes(self, data):
        return self.quotes

    @http.route
    def get_candles(self, data):
        api = self.apis['BitMEX']
        return api.get_candles(data['sym'])

    @http.route
    def post_limit(self, data):
        api = self.apis['BitMEX']
        api.create_limit_order(
            data['sym'],
            data['side'],
            data['size'],
            data['price']
        )

    @http.route
    def post_tradingview(self, data):
        api = self.apis['BitMEX']
        api.create_market_order(
            data['sym'],
            data['side'],
            data['size']
        )        


if __name__ == '__main__':
    bot = Trading()
    bot.start()
