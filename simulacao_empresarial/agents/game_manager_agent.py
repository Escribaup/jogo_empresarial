from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pandas as pd
from .accountant_agent import AccountantAgent
from .economy_agent import EconomyAgent
from .competitor_agent import CompetitorAgent

class GameManagerAgent:
    def __init__(self):
        self.economy_agent = EconomyAgent()
        self.competitor_agent = CompetitorAgent()
        self.accountant = AccountantAgent()
        self.initialize_game_state()
        self.df = pd.DataFrame(columns=['quarter', 'economy', 'competitors', 'financials', 'analysis', 'decisions'])
        self.agent = self.create_agent()

    def create_agent(self):
        return create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
            self.df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix="Você é um analista de negócios experiente. Analise os dados do jogo e forneça insights.",
            allow_dangerous_code=True  # Adicionando este parâmetro
        )

    def initialize_game_state(self):
        self.game_state = {
            "quarter": 0,
            "factory_capacity": 3000,  # 1000 unidades/mês * 3 meses por trimestre
            "employees": 10,
            "production_cost_per_unit": 10,
        }

    def run_game(self, player_decisions):
        try:
            self.game_state["quarter"] += 1
            current_quarter = self.game_state["quarter"]
            
            # Simular a economia
            economy_data = self.economy_agent.simulate(self.df)
            
            # Simular competidores
            competitors_data = self.competitor_agent.simulate(self.df)
            
            # Processar decisões do jogador e registrar transações
            self.process_player_decisions(player_decisions, current_quarter)
            
            # Gerar relatórios financeiros
            financial_reports = self.accountant.generate_financial_statements()
            financial_analysis = self.accountant.analyze_financial_position()
            
            # Adicionar nova linha ao DataFrame
            new_row = pd.DataFrame({
                'quarter': [current_quarter],
                'economy': [economy_data],
                'competitors': [competitors_data],
                'financials': [financial_reports],
                'analysis': [financial_analysis],
                'decisions': [str(player_decisions)]
            })
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            
            # Executar o agente para análise e recomendações
            query = f"Analise os dados do trimestre {current_quarter}, incluindo os relatórios financeiros detalhados e a análise financeira, e forneça um resumo da situação atual e recomendações para o próximo trimestre."
            result = self.agent.run(query)
            
            return result
        except Exception as e:
            print(f"Erro ao executar o jogo: {e}")
            return f"Desculpe, ocorreu um erro ao executar o jogo: {str(e)}"

    def process_player_decisions(self, player_decisions, current_quarter):
        date = f"Q{current_quarter}"
        
        # Calcular produção real (limitada pela capacidade da fábrica)
        production = min(player_decisions['production'], self.game_state['factory_capacity'])
        
        # Calcular vendas (simplificação: assumindo que todas as unidades produzidas são vendidas)
        sales_units = production
        sales_revenue = sales_units * player_decisions['price']
        
        # Registrar transações
        self.accountant.record_transaction(date, 'Sales', 0, sales_revenue, 'Revenue from sales')
        self.accountant.record_transaction(date, 'Cash', sales_revenue, 0, 'Cash from sales')
        
        # Custos de produção
        production_cost = production * self.game_state['production_cost_per_unit']
        self.accountant.record_transaction(date, 'COGS', production_cost, 0, 'Cost of goods sold')
        self.accountant.record_transaction(date, 'Cash', 0, production_cost, 'Payment for production costs')
        
        # Despesas de marketing
        self.accountant.record_transaction(date, 'Marketing Expense', player_decisions['marketing'], 0, 'Marketing expenses')
        self.accountant.record_transaction(date, 'Cash', 0, player_decisions['marketing'], 'Payment for marketing')
        
        # Investimentos em P&D
        self.accountant.record_transaction(date, 'R&D Expense', player_decisions['research'], 0, 'R&D expenses')
        self.accountant.record_transaction(date, 'Cash', 0, player_decisions['research'], 'Payment for R&D')
        
        # Investimentos em capacidade
        if player_decisions['capacity_investment'] > 0:
            self.accountant.record_transaction(date, 'Property, Plant & Equipment', player_decisions['capacity_investment'], 0, 'Investment in capacity')
            self.accountant.record_transaction(date, 'Cash', 0, player_decisions['capacity_investment'], 'Payment for capacity investment')
            self.game_state['factory_capacity'] += player_decisions['capacity_investment'] // 100  # Assumindo que cada 100 unidades de investimento aumentam a capacidade em 1 unidade
        
        # Doações
        if player_decisions['donations'] > 0:
            self.accountant.record_transaction(date, 'Charitable Donations', player_decisions['donations'], 0, 'Charitable donations')
            self.accountant.record_transaction(date, 'Cash', 0, player_decisions['donations'], 'Payment for donations')
        
        # Atualizar o estado do jogo
        self.game_state['production_cost_per_unit'] = max(8, self.game_state['production_cost_per_unit'] - 0.1)  # Redução de custo com a experiência, mínimo de 8
