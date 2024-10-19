from game_data.company import Company
from game_data.economy import Economy
import random

class GameManager:
    def __init__(self, player_name):
        self.company = Company(player_name, 10000)
        self.economy = Economy()
        self.current_quarter = 1
        self.history = []
        self.market_share = 50  # Inicialmente, o jogador tem 50% do mercado
        self.competitors = [Company(f"Competidor {i}", 10000) for i in range(1, 4)]  # 3 competidores

    def play_quarter(self, price, production, marketing, capacity_investment, research, donations):
        # Atualizar decisões da empresa do jogador
        self.company.set_decisions(price, production, marketing, capacity_investment, research, donations)
        
        # Simular a economia
        self.economy.simulate_market()
        
        # Calcular a demanda total do mercado
        base_demand = self.economy.calculate_base_demand()
        market_multiplier = self.economy.get_market_multiplier()
        total_market_demand = int(base_demand * market_multiplier)
        
        # Calcular a demanda do jogador
        player_demand = self.economy.calculate_demand(price, marketing)
        player_demand = int(player_demand * (self.market_share / 100))
        player_demand = min(player_demand, self.company.production)  # Limitar à produção
        
        # Calcular receita e custos
        revenue = player_demand * price
        production_cost = self.company.production * 50  # Custo de produção por unidade
        total_costs = production_cost + marketing + research + donations
        
        # Calcular lucro
        profit = revenue - total_costs
        
        # Atualizar o saldo da empresa
        self.company.balance += profit
        
        # Atualizar market share baseado nas decisões
        market_influence = (marketing / 10000) - (price / 100) + (research / 5000)
        self.market_share = max(0, min(100, self.market_share + market_influence))

        # Preparar o resultado do trimestre
        result = {
            "quarter": self.current_quarter,
            "market_condition": self.economy.market_condition,
            "total_market_demand": total_market_demand,
            "player_demand": player_demand,
            "revenue": revenue,
            "production_cost": production_cost,
            "total_costs": total_costs,
            "profit": profit,
            "balance": self.company.balance,
            "market_share": self.market_share,
            "price": price,
            "production": production,
            "marketing": marketing,
            "capacity": self.company.capacity,
            "research": research,
            "donations": donations
        }
        
        self.history.append(result)
        self.current_quarter += 1
        
        return result

    def get_financial_report(self):
        if not self.history:
            return None
        
        latest = self.history[-1]
        previous = self.history[-2] if len(self.history) > 1 else None
        
        def safe_percentage_change(new, old):
            if old == 0:
                return "N/A" if new == 0 else "∞"
            return f"{((new - old) / old) * 100:.2f}%"
        
        report = {
            "Revenue": latest["revenue"],
            "Costs": latest["total_costs"],
            "Profit": latest["profit"],
            "Balance": latest["balance"],
            "Market Share": f"{latest['market_share']:.2f}%",
            "Capacity": latest["capacity"],
            "Demand": latest["player_demand"],
            "Production": latest["production"],
            "Sales": min(latest["player_demand"], latest["production"])
        }
        
        if previous:
            report.update({
                "Revenue Change": safe_percentage_change(latest['revenue'], previous['revenue']),
                "Profit Change": safe_percentage_change(latest['profit'], previous['profit']),
                "Market Share Change": f"{latest['market_share'] - previous['market_share']:.2f}%"
            })
        
        return report

    def get_market_report(self):
        if not self.history:
            return None
        
        latest = self.history[-1]
        
        return {
            "Market Condition": latest["market_condition"],
            "Total Market Demand": latest["total_market_demand"],
            "Player Demand": latest["player_demand"],
            "Player Price": latest["price"],
            "Market Share": f"{latest['market_share']:.2f}%"
        }
