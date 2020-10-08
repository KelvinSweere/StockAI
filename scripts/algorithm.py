from data_collecting import DataCollecting
import numpy as np

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
        self.MA = self.data.rolling(window=self.npoints).mean()

    def getMA(self):
        try:
            self.MA
        except AttributeError:
            print("Set first MA before getting it.")
        else:
            return self.MA
            
    def setRSI(self):
        """Calculates relative strenght index (RSI) with npoints.
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
        self.RSI = 100-100/(1+RS_up/RS_down)

    def getRSI(self):
        try:
            self.RSI
        except AttributeError:
            print("Set first RSI before getting it.")
        else:
            return self.RSI

    def setBB(self, sigma=1):
        #set bollingbands (1sigma)

        # return (BB_up, BB_down)
        pass

    def getBB(self):
        pass


if __name__ == "__main__":

    stock_name = 'RDSA.AS'
    dc = DataCollecting(stock_name, "1d", "1m")
    data = dc.getData()

    fig_RSI, ax = plt.subplots()
    plt.plot(data['Open'])
    plt.show()

    # fig_RSI, ax = plt.subplots()

    al = Algorithm(data) 
    al.setNpoints(7)

    al.setRSI()
    RSI = al.getRSI()

    plt.plot(RSI)

    al.setNpoints(14)

    al.setRSI()
    RSI = al.getRSI()

    plt.plot(RSI)
    plt.show()
    
