# data/market_data.py

class MarketData:
    def __init__(self):
        self.data = {}

    def add_market(self, market_name):
        if market_name not in self.data:
            self.data[market_name] = {
                'timeframe': '',
                'data_source': '',
                'optimisation_timespan': '',
                'out_of_sample_timespan': '',
                'equity_curve': None,
                'performance_metrics': None,
                'notes': ''
            }

    def remove_market(self, market_name):
        if market_name in self.data:
            del self.data[market_name]

    def get_markets(self):
        return list(self.data.keys())

    def set_market_data(self, market_name, key, value):
        if market_name not in self.data:
            self.add_market(market_name)
        self.data[market_name][key] = value

    def get_market_data(self, market_name):
        return self.data.get(market_name, None)

    def get_all_data(self):
        return self.data

    def clear_all_markets(self):
        self.data.clear()