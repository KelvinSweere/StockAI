
class InvestmentPortfolio():

    def __init__(self, start_val=30):
        self.paid_up_cap = start_val  # 30 euro startkapitaal.
        self.cash = start_val

        self.stock_num = 0
        self.stock_money = 0

        self.printBool = False
        self.TAKER_FEE = 0.26 / 100  #0.16% KRAKEN

    def buy_whole_stocks(self, price):
        """Buy stocks with price per stock.

        Args:
            price (float): price per stock.
        """
        if(self.cash > price):
            return False
        else:
            stock_that_can_be_bought = self.cash / price

            fee_price = stock_that_can_be_bought * price * self.TAKER_FEE

            if(self.stock_money - stock_that_can_be_bought * price - fee_price < 0 ):
                stock_that_can_be_bought-=1

            print(str(int(stock_that_can_be_bought)) +
                    " stocks bought with a price of €" + str(price) + 
                    " with fee price of €" + str(fee_price))

            self.stock_num = int(stock_that_can_be_bought)
            self.stock_money = self.stock_num * price + fee_price
            self.cash = self.cash - self.stock_num * price

            if(self.printBool):
                self.print_values()

            return True
        
    def buy(self, price, num):
        """Buy stock with price per stock and num. 

        Args:
            price (float): price per stock
            num (float): number of stocks (can be float value)
        """
        total_stock_price = price * num
        fee_price = round(total_stock_price * self.TAKER_FEE,2)

        spending_money = total_stock_price + fee_price
        
        print(str(spending_money) + " = " + str(total_stock_price) + " + " + str(round(fee_price,2)))

        if(spending_money > self.cash): 
            print("Can't be bought! Adjust number of stocks.")   
            return False  
        else:
            self.cash -= round(fee_price,2)
            self.cash -= price * num
            self.stock_num += num

            print("stock num = " + str(self.stock_num))
            print("cash = " + str(self.cash))
            return True


    def sell_all(self, price):
        """Sell all stocks with price parameter.

        Args:
            price (float): Price per stock.
        """
        bol = self.sell(price=price, num=self.stock_num)
        return bol

    def sell(self, price, num):
        """Sell stocks with price and number of stocks.

        Args:
            price (float): price of stocks.
            num (float): number of stocks (can be float value with currency).
        """
        if(num > self.stock_num):
            print("Invalid number. Change number of stocks to sell.")
            return False
        else:
            print(str(round(self.stock_num, 4)) + 
                " stocks sold with a price of €" + str(price) + " per coin")
            fund_to_cash = price * num - round(price * num * self.TAKER_FEE, 2) 

            self.cash += fund_to_cash
            self.stock_num -= num  
            #new stock value...
            self.stock_money = price * self.stock_num  


            print("Cash status = " + str(self.cash))

            return True

    def print_return_class(self):
        """Print return of investment in %.

        Returns:
            None
        """
        returns = (((self.cash + self.stock_money) -
            self.paid_up_cap) / self.paid_up_cap) * 100

        print("Current return value = " + str(round(returns, 2)) + "%")
        return returns

    def get_return_stock(self, price, num):
        """return the returnsvalue of stock.

        Args:
            price (float): price of one stock.
            num (float): number of stocks. Is a float because of the crypto currancy.

        Returns:
            returns: returnvalue in percentage.
        """
        returns = (((self.cash + price * num) -
            self.paid_up_cap) / self.paid_up_cap) * 100

        return returns

    def print_values(self):
        """Print all important values.

        Returns:
            None
        """
        print("Current cash = " + str(self.cash))
        print("Current stocks = "+ str(self.stock_num))
        print("With a total stock value of = " + str(self.stock_money))
        print("\n")

    def deposit_cash(self, cash):
        """Send cash to portfolio class.

        Args:
            cash (float): total value of cash that will be added (+) to account.
        """
        self.cash += cash
        self.paid_up_cap += cash
        print("New cash status = " + str(self.cash))    

    def withdraw_cash(self, cash):
        """Get cash from portfolio

        Args:
            cash (float): total value of cash that will be get (-) from account.
        """
        if(self.cash - cash < 0):
            print("Invalid option")
        else:
            self.cash -= cash
            print("New cash status = " + str(self.cash))

if __name__ == "__main__":
    xrp = InvestmentPortfolio(31)

    # eth.buy(price=312.46, num=0.09547)    #buy date = 20 oct
    # eth.buy(price=293.28, num=0.1010)    #buy date = 20 oct
    
    #FIXME: buy whole stock 
    # xrp.buy_whole_stocks(price=0.21229)
    xrp.buy(price=0.21229, num=145)

    # eth.sell_all(325.20)   #sell date = 29 apr
    xrp.sell(price=0.21580, num=int(xrp.stock_num/2))
    # eth.sell(price=301.75, num=float(eth.stock_num/2))

    xrp.print_return_class()

    xrp.sell_all(price=0.21736)

    """
    eth.buy(0.15582, 100)    #buy date = 27 jun
    eth.sell(0.19118)   #sell date = 27 jul
    """

    xrp.print_return_class()

    print("cash = ", xrp.cash)
    
