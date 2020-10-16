from data_collecting import DataCollecting
from algorithm import Algorithm
import matplotlib.pyplot as plt

stock_name = 'RDSA.AS'
dc = DataCollecting(stock_name, "5d", "1m")
data = dc.getData()


al = Algorithm(data)
al.setNpoints(14)
al.setRSI()

RSI = al.getRSI()
plt.plot(data['Day'], RSI)
plt.show()
