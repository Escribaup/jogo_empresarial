import os
from dotenv import load_dotenv
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pandas as pd
from .accountant_agent import AccountantAgent
from .economy_agent import EconomyAgent
from .competitor_agent import CompetitorAgent
import ast

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class GameManagerAgent:
    def __init__(self):
        # Verifica se a chave da API está definida
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("A chave da API da OpenAI não está definida. Por favor, configure a variável de ambiente OPENAI_API_KEY.")
        
        self.economy_agent = EconomyAgent()
        self.competitor_agent = CompetitorAgent()
        self.accountant = AccountantAgent()
        self.factory_capacity = 3000  # Defina um valor padrão para a capacidade da fábrica
        self.df = pd.DataFrame()
        self.initial_state()

    def create_agent(self):
        return create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-4o-mini"),
            self.df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix="Você é um analista de negócios experiente. Analise os dados do jogo e forneça insights.",
            allow_dangerous_code=True
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
            
            # Gerar análise financeira
            financial_analysis = self.accountant.analyze_financial_position()
            
            # Atualizar o estado do jogo
            self.game_state.update({
                'economy': economy_data,
                'competitors': competitors_data,
                'financials': financial_reports,
                'analysis': financial_analysis
            })
            
            # Atualizar o DataFrame
            new_row = pd.DataFrame([self.game_state])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            
            # Imprimir o razão contábil para debug
            self.accountant.print_ledger()
            
            return self.game_state
        except Exception as e:
            print(f"Erro ao executar o jogo: {e}")
            return f"Desculpe, ocorreu um erro ao executar o jogo: {str(e)}"

    def process_player_decisions(self, player_decisions, current_quarter):
        try:
            # Produção
            production = min(player_decisions.get('production', 0), self.factory_capacity)
            production_cost = production * 10  # Assumindo um custo de 10 por unidade

            # Contabilizar custo de produção
            self.accountant.record_transaction(f'Q{current_quarter}', 'Inventory', production_cost, 0, 'Production added to inventory')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Cash', 0, production_cost, 'Payment for production costs')

            # Vendas
            sales_price = player_decisions.get('price', 0)
            marketing_expense = player_decisions.get('marketing', 0)
            sales = production  # Assumindo que todas as unidades produzidas são vendidas

            sales_revenue = sales * sales_price

            # Contabilizar receita de vendas
            self.accountant.record_transaction(f'Q{current_quarter}', 'Cash', sales_revenue, 0, 'Cash from sales')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Sales', 0, sales_revenue, 'Revenue from sales')

            # Contabilizar custo das mercadorias vendidas (COGS)
            self.accountant.record_transaction(f'Q{current_quarter}', 'COGS', production_cost, 0, 'Cost of goods sold')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Inventory', 0, production_cost, 'Reduction in inventory due to sales')

            # Contabilizar despesas de marketing
            self.accountant.record_transaction(f'Q{current_quarter}', 'Marketing', marketing_expense, 0, 'Marketing expenses')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Cash', 0, marketing_expense, 'Payment for marketing')

            # Outras decisões do jogador (R&D, doações, etc.)
            rd_expense = player_decisions.get('research_development', 0)
            donations = player_decisions.get('charitable_giving', 0)

            self.accountant.record_transaction(f'Q{current_quarter}', 'R&D', rd_expense, 0, 'R&D expenses')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Cash', 0, rd_expense, 'Payment for R&D')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Donations', donations, 0, 'Charitable donations')
            self.accountant.record_transaction(f'Q{current_quarter}', 'Cash', 0, donations, 'Payment for donations')

        except Exception as e:
            print(f"Erro ao processar decisões do jogador: {e}")

    def initial_state(self):
        self.game_state = {
            'quarter': 0,
            'financials': self.accountant.generate_financial_statements(),
        }
        self.accountant.print_ledger()  # Imprime o razão contábil para debug

    def get_last_financial_reports(self):
        if not self.df.empty:
            last_financials = self.df.iloc[-1]['financials']
            if isinstance(last_financials, str):
                # Se for uma string, tenta converter para dicionário
                try:
                    return ast.literal_eval(last_financials)
                except:
                    print("Erro ao converter relatórios financeiros de string para dicionário")
                    return {}
            return last_financials
        return {}
