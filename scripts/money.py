
class InvestmentPortfolio():

    def __init__(self, start_val=30):
        self.paid_up_cap = start_val  # 30 euro startkapitaal.
        self.cash = start_val

        self.stock_num = 0
        self.stock_money = 0

        self.printBool = False
        self.FEE = 0.16 / 100  #0.16% KRAKEN

    def buy(self, price):
        """Buy stocks with price per stock.

        Args:
            price (float): price per stock.
        """
        stock_that_can_be_bought = self.cash / price

        fee_price = stock_that_can_be_bought * price * self.FEE

        if(self.stock_money - stock_that_can_be_bought * price - fee_price < 0 ):
            stock_that_can_be_bought-=1

        print(str(int(stock_that_can_be_bought)) +
              " stocks bought with a price of €" + str(price) + 
              " with fee price of €" + str(fee_price))

        self.stock_num = int(stock_that_can_be_bought)
        self.stock_money = self.stock_num * price + fee_price
        self.cash = self.cash - self.stock_num * price

        if(self.printBool):
            self.printValues()


    def sell(self, price):
        """Sell all stocks with price parameter.

        Args:
            price (float): Price per stock.
        """
        print(str(int(self.stock_num)) +
              " stocks sold with a price of €" + str(price))
        self.cash += price * self.stock_num
        self.stock_money = 0 #sell all.
        self.stock_num = 0  #reset stocks.

        if(self.printBool):
            self.printValues()
        
        print("Cash status = " + str(self.cash))

    def printReturn(self):
        """Print return of investment in %.

        Returns:
            None
        """
        returns = (((self.cash + self.stock_money) -
               self.paid_up_cap) / self.paid_up_cap) * 100

        print("Current return value = " + str(round(returns, 2)) + "%")

    def printValues(self):
        """Print all important values.

        Returns:
            None
        """
        print("Current cash = " + str(self.cash))
        print("Current stocks = "+ str(self.stock_num))
        print("With a stock value of = " + str(self.stock_money))
        print("\n")

    def depositCash(self, cash):
        """Send cash to current portfolio.

        Args:
            cash (float): total value of cash that will be added (+) to account.
        """
        self.cash += cash
        self.paid_up_cap += cash
        print("New cash status = " + str(self.cash))    

    def takeCash(self, cash):
        """Get cash from current portfolio

        Args:
            cash (float): total value of cash that will be get (-) from account.
        """
        if(self.cash - cash < 0):
            print("Invalid option")
        else:
            self.cash -= cash
            print("New cash status = " + str(self.cash))

if __name__ == "__main__":
    #riple
    rpl = InvestmentPortfolio()

    rpl.buy(0.12278)    #buy date = 12 mar
    rpl.sell(0.20880)   #sell date = 29 apr

    rpl.buy(0.15582)    #buy date = 27 jun
    rpl.sell(0.19118)   #sell date = 27 jul

    rpl.printReturn()

    print("cash = ", rpl.cash)
