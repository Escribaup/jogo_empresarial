import random

class Economy:
    def __init__(self):
        self.market_condition = "stable"
        self.base_demand = 1000  # Demanda base inicial

    def simulate_market(self):
        conditions = ["weak", "stable", "strong"]
        self.market_condition = random.choice(conditions)
        
        # Ajusta a demanda base com base na condição do mercado
        if self.market_condition == "weak":
            self.base_demand = max(800, self.base_demand - random.randint(50, 200))
        elif self.market_condition == "strong":
            self.base_demand = min(1200, self.base_demand + random.randint(50, 200))
        else:
            self.base_demand = max(800, min(1200, self.base_demand + random.randint(-50, 50)))

    def calculate_base_demand(self):
        return self.base_demand

    def get_market_multiplier(self):
        if self.market_condition == "weak":
            return random.uniform(0.8, 1.0)
        elif self.market_condition == "strong":
            return random.uniform(1.0, 1.2)
        else:
            return random.uniform(0.9, 1.1)

    def calculate_demand(self, price, marketing):
        base_demand = self.calculate_base_demand()
        price_effect = max(0, 1 - (price / 100))
        marketing_effect = min(2, 1 + (marketing / 10000))
        market_multiplier = self.get_market_multiplier()
        
        return int(base_demand * price_effect * marketing_effect * market_multiplier)
