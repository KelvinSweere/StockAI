import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd

class DataCollecting():

    def __init__(self, tckr_name, period, interval):
        #check if tckr is legal.
        if not (self._check_if_tck_legal(tckr_name)):
            print("tckr is NOT legal...")
        else:
            print("tckr is legal...")
            self.tckr_name = tckr_name
            self.tckr = yf.Ticker(tckr_name.upper())

            self.data = self.tckr.history(period=period, interval=interval, dtype=np)
            self.calculate_delta()  # calculate difference open, close.
            # self._plot_figure()
            # plt.show()

            self.data['Day'] = np.arange(0, len(self.data))

            self.period_str = str(period)
            self.interval_str = str(interval)

            #change time to interger value to plot RSI and more than one date.

            # self.data.index = self.data.dt.days.astype('int16')

            #delete ticker and return value
        super().__init__()

    def _check_if_tck_legal(self, tckr_name):
        """Checks if Yahoo can get data.

        Args:
            tckr_name (str): name of the Yahoo ticker. 

        Returns:
            bool: true if data is found, false if not data is found.
        """
        try:
            tckr = yf.Ticker(tckr_name.upper())
            
            check_info = tckr.history(period='1d', interval='1d')   #one datapoint.

        #TODO: print sector.  (not downloaded jet.)

        except KeyError:
            print("Ticker " + str(tckr_name) + " is found.")
            return 1
        except IndexError:
            print("No information found about ticker " + str(tckr_name))
            return 0

        else:
            if(check_info.empty):
                return 0
            else:
                print("Ticker " + str(tckr_name) + " is found.")
                return 1

    def plot_figure(self):
        mpf.plot(self.data, type='candle', style='charles',
                title=self.tckr_name,
                ylabel='Price (€)',
                ylabel_lower='Shares \nTraded',
                mav=(6, 6, 9))
        
        plt.show()
        """
        plt.figure(figsize=(15, 5))
        plt.plot(self.data['Open'],'ro-', label='line 1', linewidth=0.5)
        plt.plot(self.data['Close'],'bo-', label='line 1', linewidth=0.5)
        plt.grid(True)
        plt.xlabel("Date")
        plt.ylabel("€")
        plt.show()
        """

    def get_data(self):
        return self.data

    def calculate_delta(self):
        self.data.insert(6, "Delta", self.data['Open']-self.data['Close'], True)
    
    # def getIndex(self):
    #     return self.data.index


if __name__ == "__main__":
    # stock_name = input("Stock name... ")

    """
    interval = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    period = 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    """

    #TODO: first scope, 1d 1m prediction. 
    #TODO: goal monthly prediction.
    stock_name = 'RDSA.AS'
    dc = DataCollecting(stock_name, "5d", "1h")
    dc.plot_figure()




