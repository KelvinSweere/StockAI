import yfinance as yf
import matplotlib.pyplot as plt

class dataCollecting():

    def __init__(self, tckr_name, period):
        #check if tckr is legal.
        if not (self._checkIfTckLegal(tckr_name)):
            print("tckr is NOT legal...")
        else:
            print("tckr is legal...")
            self.tckr_name = tckr_name
            self.tckr = yf.Ticker(tckr_name.upper())

            self.data = self.tckr.history(period=period)

            self._plot_figure(self.data['Open'], color="ro-")
            self._plot_figure(self.data['Close'], new=False, color="bo-")
            plt.show()

            #delete ticker and return value
        super().__init__()

    def _checkIfTckLegal(self, tckr_name):
        try:
            tckr = yf.Ticker(tckr_name.upper())
            
            check_info = "not found"

            #TODO: check of goede info aankomt.
            check_info = tckr.history(period='1min')
            print('check_info = ' + check_info)

        except KeyError:
            print("Ticker " + str(tckr_name) + " is found.")
            return 1
        except IndexError:
            print("No information found about ticker " + str(tckr_name))
            return 0

        else:
            if(check_info != "No data found, symbol may be delisted"):
                #TODO: print sector.
                print("Ticker " + str(tckr_name) + " is found.")
                return 1
            else: 
                return 0

    def _plot_figure(self, data, new=True, color="ro-", x_axis_name="Date", y_axis_name="€"):
        #TODO: add name stock.

        if(new==True):
            plt.figure(figsize=(15, 5))

        plt.plot(data, color, label='line 1', linewidth=0.5)
        plt.grid(True)
        plt.xlabel(x_axis_name)
        plt.ylabel(y_axis_name)
                


if __name__ == "__main__":
    # stock_name = input("Stock name... ")
    stock_name = 'RDSA.A'
    dc = dataCollecting(stock_name, "2mo")

