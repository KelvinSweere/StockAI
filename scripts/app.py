from data_collecting import DataCollecting
from money import InvestmentPortfolio
from algorithm import Algorithm
import matplotlib.pyplot as plt
import numpy as np

stock_name = 'XRP-EUR'
dc = DataCollecting(stock_name, "1mo", "1h")
data = dc.get_data()

print("data punten = " + str(len(data.index)))
print("Laatste datapunt = " + str(data.index[-1]))

al = Algorithm(data) 

al.set_npoints(20)
al.set_BB()
al.set_npoints(14)
al.set_RSI()
# al.plot_all()

RSI = al.get_RSI()
BB_up, BB_down = al.get_BB()

#TODO: buy when price is under 30, sell when price is above 70.

port2 = InvestmentPortfolio(30)

port2.buy(price=data['Close'][0], num=100)

high_rend, highest_val_procent = 0, 0

start, end = 0.0, 10.0
delta = 0.1

som_for_linespace = (end-start) / delta + 1

array_prc = np.linspace(start, end, int(som_for_linespace))

for val_procent in array_prc:  #from 0.0% to 0.2% with 0.1% steps.

    port = InvestmentPortfolio(30)

    for RSI_percentage, day in zip(RSI, range(0,len(RSI))):
        #to buy = <2 std_dev.
        #to sell = >2 std_dev
        # if(day > 20):
        if(RSI_percentage <= 30.0):
            #buy...
            # print("RSI < 30")
            if(data['Close'][day] < BB_down[day]):
                # bol = port.buy(price=data['Close'][day], num=100)
                bol = port.buy_whole_stocks(price=data['Close'][day])

                if(bol):
                    print("buy stock..." + str(day) + "\n")
                
        elif(RSI_percentage>=70.0):
            #uperband_cnt
            # print("RSI > 70")
            ret_value = port.get_return_stock(data['Close'][day], port.stock_num)
            if(data['Close'][day] < BB_up[day] and ret_value >= val_procent):
                bol = port.sell_all(price=data['Close'][day])

                if(bol):
                    print("sell stock on day..." + str(day) + " for price = " + str(data['Close'][day]) + "\n")

    port.sell_all(data['Close'][-1])
    rend = port.print_return_class()
        
    if(rend > high_rend):
        print("!!! ~~~")
        port.print_return_class()
        print("rend = " + str(rend))
        print("~~~!!!")

        high_rend = rend 
        highest_val_procent = val_procent

port2.sell_all(data['Close'][-1]) #sell all on the last day to validate the other values.

print("\n RETURN VALUE BHS")
port2.print_return_class()
print("\n RETURN VALUE ALGORITHM")
print("Highest rend = " + str(round(high_rend,2)) + "%")
print("Sell percentage calculated = " + str(round(highest_val_procent,2)) + "%")

#"3mo", "1h"
#highest rend = 7.801264174779258
#highest val procent = 5.5