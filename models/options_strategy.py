class OptionsStrategy:
    def __init__(self, stock_price, strike_price, premium, current_volatility, risk_appetite):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.premium = premium
        self.current_volatility = current_volatility
        self.risk_appetite = risk_appetite  # Scale of 0-1, where 1 is very aggressive.

    def covered_call(self):
        """
        Implement a covered call strategy:
        - Sell call options on stocks you already own.
        - Suitable when expecting the stock price to rise moderately or remain stable.
        """
        if self.stock_price <= self.strike_price and self.current_volatility > 0.2:
            income = self.premium * 100  # Assuming 1 option contract covers 100 shares.
            print(f"Sell a covered call to earn an income of {income}.")
            return "Sell Covered Call", income
        else:
            return "No Action", 0

    def protective_put(self):
        """
        Implement a protective put strategy:
        - Buy put options to protect against a decline in stock price.
        - Suitable when you own the stock and are worried about potential downsides.
        """
        if self.stock_price >= self.strike_price and self.current_volatility > 0.3:
            cost = self.premium * 100  # Assuming 1 option contract covers 100 shares.
            print(f"Buy a protective put to hedge against price drop at a cost of {cost}.")
            return "Buy Protective Put", -cost
        else:
            return "No Action", 0

# Example usage
if __name__ == "__main__":
    strategy = OptionsStrategy(stock_price=150, strike_price=155, premium=2, current_volatility=0.25, risk_appetite=0.5)
    action, value = strategy.covered_call()
    print(action, value)

    action, value = strategy.protective_put()
    print(action, value)
