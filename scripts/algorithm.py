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
        self.MA = self.data.rolling(window=self.npoints).mean()

    def getMA(self):
        try:
            self.MA
        except AttributeError:
            print("Set first MA before getting it.")
        else:
            return self.MA
            
    def setRSI(self):
        #Relative strenght index.
        #70 is overbought, 30 oversold.
        pass

    def getRSI(self):
        pass

    def setBB(self, sigma=1):
        #set bollingbands (1sigma)
        pass

    def getBB(self):
        pass


if __name__ == "__main__":

    def test_MA():
        stock_name = 'RDSA.AS'
        dc = DataCollecting(stock_name, "1d", "1m")
        data = dc.getData()

        al = Algorithm(data["Open"]) 
        al.setNpoints(7)
        
        al.setMA()
        MA = al.getMA()


        plt.plot(MA, color="r")
        plt.plot(data["Open"], color="b")

        al.setNpoints(14)

        al.setMA()
        MA2 = al.getMA()

        plt.plot(MA2, color="g")
        plt.plot(data["Open"], color="b")
        plt.show()
    
    test_MA()
