
class CLI():
    def __init__(self):
        super().__init__()

    def _checkIfPeriodLegal(self, period):
        #check month...

        #check string format
        return 1


if __name__ == "__main__":
    periode = "1mot"
    interval = "1m"

    if(periode.find("mo") != -1):
        #TODO: check if value is infront
        #TODO: check if only values....
        per = periode;
    elif(periode.find("y") != -1):
        #check if value is infront
        per = periode
    else:
        print("invalid operator. Check documentation.")

    pass
