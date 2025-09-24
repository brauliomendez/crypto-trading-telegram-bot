import ccxt
from datetime import datetime
import env_secrets

class Exchange:
    def __init__(self, simulated=False, logs_file="orders.log"):
        self.__simulated=simulated
        self.__logs_file=logs_file
        self.__ex = ccxt.binance({
            'apiKey': env_secrets.BINANCE_API_KEY,
            'secret': env_secrets.BINANCE_SECRET_KEY,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        self.__ex.load_markets()
        self.__buy_order_info = {}
        self.__sell_order_info = {}

    def fetch_ticker(self, symbol):
        ticker = self.__ex.fetch_ticker(symbol)
        return ticker["last"]

    def __get_fee_usdc(self, order):
        fee = order['fees'][0]['cost']
        bnb_price = self.fetch_ticker("BNB/USDC")
        fee_usdc = fee * bnb_price
        return fee_usdc
    
    def __print_log(self, line):
        with open(self.__logs_file, "a") as f:
            f.write(f"{line}\n")

    def buy(self, symbol, quote_amount, simulated_price=None):
        if not self.__simulated:
            # Real
            try:
                order = self.__ex.create_order(symbol=symbol,type="market",side="buy",amount=None,params={"quoteOrderQty": quote_amount})
            except Exception as e:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                self.__print_log(f"\n[{now}] Error buying {quote_amount}$ of {symbol}:\n{e}\n")
                raise

            cost = order['cost']
            usdc_fee = self.__get_fee_usdc(order)
            self.__buy_order_info = {
                "purchased_amount": float(order['amount']),
                "price": order['price'],
                "cost": cost,
                "usdc_fee": usdc_fee,
                "fee_percentage": usdc_fee / cost * 100,
                "total_cost": cost + usdc_fee
            }
        else:
            # Simulated
            usdc_fee = quote_amount * 0.075 / 100
            self.__buy_order_info = {
                "purchased_amount": quote_amount / simulated_price,
                "price": simulated_price,
                "cost": quote_amount,
                "usdc_fee": usdc_fee,
                "fee_percentage": 0.075,
                "total_cost": quote_amount + usdc_fee
            }
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.__print_log(f"""### INIT BUY ###

[{now}]
  Purchased amount: {self.__buy_order_info['purchased_amount']} {symbol} @ {self.__buy_order_info['price']}
  Cost: {self.__buy_order_info['cost']}$
  Fee: {self.__buy_order_info['usdc_fee']}$
  Fee percentage: {self.__buy_order_info['fee_percentage']}%
  Total cost: {self.__buy_order_info['total_cost']}$

### END BUY ###
""")
        return self.__buy_order_info

    def sell(self, symbol, amount, simulated_price=None):
        if not self.__simulated:
            # Real
            try:
                order = self.__ex.create_market_sell_order(symbol=symbol, amount=amount)
            except Exception as e:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                self.__print_log(f"\n[{now}] Error selling {amount} {symbol}:\n{e}\n")
                raise

            cost = order['cost']
            usdc_fee = self.__get_fee_usdc(order)
            self.__sell_order_info = {
                "sold_amount": float(order['amount']),
                "price": order['price'],
                "cost": cost,
                "usdc_fee": usdc_fee,
                "fee_percentage": usdc_fee / cost * 100,
                "total_recovered": cost - usdc_fee
            }
        else:
            # Simulated
            usdc_fee = amount * simulated_price * 0.075 / 100
            self.__sell_order_info = {
                "sold_amount": amount,
                "price": simulated_price,
                "cost": amount * simulated_price,
                "usdc_fee": usdc_fee,
                "fee_percentage": 0.075,
                "total_recovered": amount * simulated_price - usdc_fee
            }
        
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.__print_log(f"""### INIT SELL ###

[{now}]
  Sold amount: {self.__sell_order_info['sold_amount']} {symbol} @ {self.__sell_order_info['price']}
  Cost: {self.__sell_order_info['cost']}$
  Fee: {self.__sell_order_info['usdc_fee']}$
  Fee percentage: {self.__sell_order_info['fee_percentage']}%
  Total recovered: {self.__sell_order_info['total_recovered']}$

### END SELL ###
""")

        self.__print_log(f"""Summary:
  Operation balance without fees: {self.__sell_order_info['cost'] - self.__buy_order_info['cost']}$
  Operation fees: {self.__buy_order_info['usdc_fee'] + self.__sell_order_info['usdc_fee']}$
  Operation balance: {self.__sell_order_info['total_recovered'] - self.__buy_order_info['total_cost']}$

################################################
""")
        return self.__sell_order_info

