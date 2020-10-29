from data_collecting import DataCollecting
import numpy as np
import pandas as pd

#debugging
import matplotlib.pyplot as plt

class Algorithm():
    """Class for all the stock indicator algorithms.

    """
    def __init__(self, data, npoints=14):
        """Init

        Args:
            data ([pd.DataFrame]): Dataframe
            npoints (int, optional): days to calculate. Defaults to 14.
        """
        self.data = data
        self.npoints = npoints
        self.msg = False

    def set_msg(self, bool):
        """send messages when something changes.

        Args:
            bool (bool): True if message must turend on, False if no message.
        """
        self.msg = bool
        if(self.msg == True):
            print("Message are turend on.")

    def set_npoints(self, npoints):
        """set points for the calculation.

        Args:
            npoints (int): points that needs to be calculated.
        """
        self.npoints = npoints
        if(self.msg == True):
            print("npoints are now: ", npoints)

    def set_MA(self, MA_TYPE="EWMA"):
        """Calculates the moving average filter with npoints.
            
            Args:
                MA_TYPE (str): moving avarage type. Can be:
                                EWMA - exponential moving average
                                SMA - simple moving average 
        """
        MA_TYPE.upper()
        self.MA_TYPE = MA_TYPE
        if(MA_TYPE == "SMA"):
            self.MA = self.data["Close"].rolling(window=self.npoints).mean()
        elif(MA_TYPE == "EWMA"):
            self.MA = self.data["Close"].ewm(span=self.npoints).mean()
        else:
            print("Invalid MA_TYPE")

    def get_MA(self):
        """get moving avarage (MA)

        Returns:
            DataFrame: moving avarge data
        """
        try:
            self.MA
        except AttributeError:
            print("Set first MA before getting it.")
        else:
            return self.MA

    def append_MA(self):
        self.data['MA'] = self.MA

    def set_RSI(self, MA_TYPE="EWMA"):
        """Calculates relative strenght index (RSI) with npoints.

        MA_TYPE:
            SMA = simple moving avarge filter.
            EWMA = exponential moving average.
        
        RSI validated on 20-10-2020 with: https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
        """
        #Relative strenght index.
        #70 is overbought, 30 oversold.

        delta = self.data.Close.diff()
        up_days, down_days = delta.copy(), abs(delta.copy())

        up_days[delta <= 0] = 0.0
        down_days[delta > 0] = 0.0
        
        if(MA_TYPE == "SMA"):
            avg_up = up_days.rolling(self.npoints).mean()
            avg_down = down_days.rolling(self.npoints).mean()
        elif(MA_TYPE == "EWMA"):
            avg_up = up_days.ewm(com=self.npoints - 1, adjust=False).mean()
            avg_down = down_days.ewm(com=self.npoints - 1, adjust=False).mean()
        else:
            print("Invalid MA_TYPE")

        RS = avg_up / avg_down

        self.RSI = 100.0 - (100.0 / (1.0 + RS))


    def get_RSI(self):
        """send RSI value back of the class. 

        NOTE: first use set_RSI. Otherwise it can give back a warning.

        Returns:
            RSI: all RSI data.
        """
        try:
            self.RSI
        except AttributeError:
            print("Set first RSI before getting it.")
        else:
            return self.RSI

    def append_RSI(self):
        """Append RSI to class data.
        """
        self.data['RSI'] = self.RSI

    def plot_RSI(self,ax = False, low_band=30, high_band=70, plot_all=False):
        """Plot RSI.

        Args:
            ax (bool, optional): Append or plot everything separately. Defaults to False.
            low_band (int, optional): lower band of the RSI that will be ploted.. Defaults to 30.
            high_band (int, optional): uper band of the RSI that will be ploted. Defaults to 70.
            plot_all (bool, optional): boolean that will be used if everything will be ploted immediately. Defaults to False.
        """
        plt.plot(self.data['Day'], self.RSI)
        plt.axhline(low_band, alpha=0.5, color='r', linestyle='--')
        plt.axhline(high_band, alpha=0.5, color='r', linestyle='--')
        plt.ylim(0,100)
        if(ax == False):
            plt.show()

    def set_BB(self, sigma=2, MA_TYPE="EWMA"):
        """set Bollingerbands with npoints.

        Args:
            sigma (int, optional): Sigma value of the Bolling Bands. Defaults to 2.
            MA_TYPE (str, optional): Moving average type. See set_MA for more info. Defaults to "EWMA".
        """
        # MA = self.data["Close"].ewm(span=self.npoints).mean()
        if(MA_TYPE == "SMA"):
            self.set_MA("SMA")
        elif(MA_TYPE == "EWMA"):
            self.set_MA("EWMA")
        
        self.BB_up = self.MA + sigma * self.data['Close'].rolling(window=self.npoints).std()
        self.BB_down = self.MA - sigma * self.data['Close'].rolling(window=self.npoints).std()

    def get_BB(self):
        """return bolling band values

        Returns:
            (BB_up, BB_down): Bolling bands up, Bolling band down
        """
        return (self.BB_up, self.BB_down)

    def plot_BB(self, ax=False):
        """Plot Bollingband with closing data.
        """
        if(ax != False):
            ax.plot(self.data['Day'], self.BB_up, color='r', alpha=0.5)
            ax.plot(self.data['Day'], self.BB_down, color='r', alpha=0.5)
            ax.plot(self.data['Day'], self.MA, color='g', alpha=0.5)
            ax.plot(self.data['Day'], self.data['Close'], color='b')  
        else:
            plt.plot(self.data['Day'], self.BB_up, color='r', alpha=0.5)
            plt.plot(self.data['Day'], self.BB_down, color='r', alpha=0.5)
            plt.plot(self.data['Day'], self.MA, color='g', alpha=0.5)
            plt.plot(self.data['Day'], self.data['Close'], color='b')  
            plt.show()

    def plot_all(self):
        """Plot all indicators.
        """
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        plt.title('All algorithm structures.')
        ax1.set_title('Bollinger Bands')
        self.plot_BB(ax1)
        ax1.set_ylabel("Price")

        ax2.set_title('RSI')
        self.plot_RSI(ax2)
        ax2.set_ylabel("RSI index")

        plt.show()

if __name__ == "__main__":

    stock_name = 'ETH-EUR'
    dc = DataCollecting(stock_name, "1d", "1m")
    data = dc.get_data()

    print("data punten = " + str(len(data.index)))
    print("Laatste datapunt = " + str(data.index[-1]))
    
    al = Algorithm(data) 

    al.set_npoints(20)
    al.set_BB()
    al.set_npoints(14)
    al.set_RSI()
    al.plot_all()

