class Company:
    def __init__(self, name, initial_balance):
        self.name = name
        self.balance = initial_balance
        self.price = 0
        self.production = 0
        self.marketing = 0
        self.capacity = 1000
        self.research = 0
        self.donations = 0

    def set_decisions(self, price, production, marketing, capacity_investment, research, donations):
        self.price = price
        self.production = production
        self.marketing = marketing
        self.capacity += capacity_investment
        self.research = research
        self.donations = donations

    def calculate_profit(self, demand):
        revenue = min(demand, self.production) * self.price
        costs = self.production * 50 + self.marketing + self.research + self.donations
        profit = revenue - costs
        self.balance += profit
        return profit
