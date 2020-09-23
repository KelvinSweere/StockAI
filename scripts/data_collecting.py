import yfinance as yf

class dataCollecting():

    def __init__(self, tckr_name, period):
        #check if tckr is legal.
        if not (self._checkIfTckLegal(tckr_name)):
            print("tckr is NOT legal...")
        else:
            print("tckr is legal...")
            self.tckr_name = tckr_name
            self.tckr = yf.Ticker(tckr_name.upper())

            if not(self._checkIfPeriodLegal(period)):
                print("period invalid")
                return
            else:
                print("Hello")



            #delete ticker and return value
        super().__init__()

    def _checkIfTckLegal(self, tckr_name):
        try:
            tckr = yf.Ticker(tckr_name.upper())

            tckr_info = tckr.get_info()

        except KeyError:
            print("Ticker " + str(tckr_name) + " is found.")
            return 1
        except IndexError:
            print("No information found about ticker " + str(tckr_name))
            return 0

        else:
            print(tckr_info['sector'].lower() + " - ticker has been founded.")
            return 1

    def _checkIfPeriodLegal(self, period):
        #check string format
        return 1


if __name__ == "__main__":
    dc = dataCollecting("RDSA.AS","1m")

