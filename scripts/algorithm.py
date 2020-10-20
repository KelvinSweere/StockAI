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

    def setMsg(self, bool):
        """send messages when something changes.

        Args:
            bool (bool): True if message must turend on, False if no message.
        """
        self.msg = bool
        if(self.msg == True):
            print("Message are turend on.")

    def setNpoints(self, npoints):
        """set points for the calculation.

        Args:
            npoints (int): points that needs to be calculated.
        """
        self.npoints = npoints
        if(self.msg == True):
            print("npoints are now: ", npoints)

    def setMA(self):
        """Calculates the moving avarage filter with npoints.
        """
        self.MA = self.data["Close"].rolling(window=self.npoints).mean()

    def getMA(self):
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

    def appendMA(self):
        self.data['MA'] = self.MA

    def setRSI(self, MA_TYPE='SMA'):
        """Calculates relative strenght index (RSI) with npoints.

        MA_TYPE:
            SMA = simple moving avarge filter.
            EWMA = exponential moving average.
        
        RSI validated on 20-10-2020 with: https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
        """

        #TODO: Validate RSI values. (unit test.)
        #Relative strenght index.
        #70 is overbought, 30 oversold.

        delta = self.data.Close.diff()
        up_days = delta.copy()
        up_days[delta <= 0] = 0.0
        down_days = abs(delta.copy())
        down_days[delta > 0] = 0.0
        RS_up = up_days.rolling(self.npoints).mean()
        RS_down = down_days.rolling(self.npoints).mean()

        if(MA_TYPE == "SMA"):
            self.RSI = 100-100/(1+RS_up/RS_down)
        elif(MA_TYPE == "EWMA"):
            # Calculate the EWMA
            roll_up1 = up_days.ewm(span=self.npoints).mean()
            roll_down1 = down_days.abs().ewm(span=self.npoints).mean()
            # Calculate the RSI based on EWMA
            RS = roll_up1 / roll_down1
            self.RSI = 100.0 - (100.0 / (1.0 + RS))
        else:
            print("Wrong moving avarge indactor type")


    def getRSI(self):
        try:
            self.RSI
        except AttributeError:
            print("Set first RSI before getting it.")
        else:
            return self.RSI

    def appendRSI(self):
        self.data['RSI'] = self.RSI

    def plotRSI(self,ax = False, low_band=30, high_band=70):

        if(ax != False):
            plt.plot(self.data['Day'], self.RSI)
            plt.axhline(low_band, alpha=0.5, color='r', linestyle='--')
            plt.axhline(high_band, alpha=0.5, color='r', linestyle='--') 
        else:
            plt.plot(self.data['Day'], self.RSI)
            plt.axhline(low_band, alpha=0.5, color='r', linestyle='--')
            plt.axhline(high_band, alpha=0.5, color='r', linestyle='--')
            plt.show()

    def setBB(self):
        """set Bollingerbands with npoints.
        """
        #set bollingbands (1sigma)
        self.setMA()

        std_dev = self.MA.rolling(window=self.npoints).std()

        self.BB_up = self.MA + (std_dev * 2)
        self.BB_down = self.MA - (std_dev * 2)

    def getBB(self):
        """return bolling band values

        Returns:
            (BB_up, BB_down): Bolling bands up, Bolling band down
        """
        return (self.BB_up, self.BB_down)

    def plotBB(self, ax=False):
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

    def plotAll(self):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        plt.title('All algorithm structures.')

        ax1.set_title('Bollinger Bands')
        self.plotBB(ax1)
        ax1.set_ylabel("Price")

        ax2.set_title('RSI')
        self.plotRSI(ax2)
        ax2.set_ylabel("RSI index")

        plt.show()

if __name__ == "__main__":

    stock_name = 'USDT-EUR'
    dc = DataCollecting(stock_name, "5d", "1h")
    data = dc.getData()

    print("data punten = " + str(len(data.index)))
    print("Laatste datapunt = " + str(data.index[-1]))
    
    al = Algorithm(data) 

    al.setNpoints(14)

    al.setBB()
    al.setRSI()

    al.plotAll()

    # RSI = al.getRSI()
    #TODO: buy when price is under 30, sell when price is above 70.
    
    """
    for percentage, day in zip(data.RSI, data.days):
        #to buy = <2 std_dev.
        #to sell = >2 std_dev
        
        if(percentage <= 30):
            #buy...
            print("buy stock..." + day)

        if(percentage>=70):
            #sell.
            print("sell stock..." + day)
    """

