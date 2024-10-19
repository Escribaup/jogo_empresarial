import os
from pathlib import Path

def create_file(file_path, content=""):
    """Cria um arquivo com o conteúdo especificado."""
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Garante que o diretório existe
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def create_project_structure(base_dir):
    base_path = Path(base_dir)

    # Estrutura do projeto
    structure = {
        "game_data": {
            "__init__.py": "",
            "company.py": '''\
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
''',
            "economy.py": '''\
import random

class Economy:
    def __init__(self):
        self.market_condition = "stable"

    def simulate_market(self):
        conditions = ["weak", "stable", "strong"]
        self.market_condition = random.choice(conditions)

    def calculate_demand(self, price, marketing):
        base_demand = 1000
        price_effect = max(0, 1 - (price / 100))
        marketing_effect = min(2, 1 + (marketing / 10000))
        
        if self.market_condition == "weak":
            multiplier = 0.8
        elif self.market_condition == "strong":
            multiplier = 1.2
        else:
            multiplier = 1

        return int(base_demand * price_effect * marketing_effect * multiplier)
'''
        },
        "ai_agents": {
            "__init__.py": "",
            "game_manager.py": '''\
from game_data.company import Company
from game_data.economy import Economy

class GameManager:
    def __init__(self, player_name):
        self.company = Company(player_name, 10000)
        self.economy = Economy()
        self.current_quarter = 1

    def play_quarter(self, price, production, marketing, capacity_investment, research, donations):
        self.company.set_decisions(price, production, marketing, capacity_investment, research, donations)
        self.economy.simulate_market()
        demand = self.economy.calculate_demand(price, marketing)
        profit = self.company.calculate_profit(demand)
        self.current_quarter += 1
        return {
            "quarter": self.current_quarter - 1,
            "market_condition": self.economy.market_condition,
            "demand": demand,
            "profit": profit,
            "balance": self.company.balance
        }
''',
            "consultant.py": "# IA para dar conselhos aos jogadores",
            "news_generator.py": "# IA para gerar notícias sobre o contexto do jogo",
            "reporter.py": "# IA para compilar relatórios de desempenho do jogador"
        },
        "scenarios": {
            "__init__.py": "",
            "economic_scenarios.py": "# Definição de cenários econômicos"
        },
        "utils": {
            "__init__.py": "",
            "helpers.py": "# Funções auxiliares para uso geral"
        },
        "tests": {
            "__init__.py": "",
            "test_company.py": "# Testes para a classe Company",
            "test_economy.py": "# Testes para a classe Economy",
            "test_ai_agents.py": "# Testes para os agentes de IA"
        },
        "frontend": {
            "__init__.py": "",
            "app.py": '''\
import streamlit as st
from ai_agents.game_manager import GameManager

def main():
    st.title("Simulador Empresarial")

    if 'game_manager' not in st.session_state:
        player_name = st.text_input("Digite o nome da sua empresa:")
        if st.button("Iniciar Jogo"):
            st.session_state.game_manager = GameManager(player_name)

    if 'game_manager' in st.session_state:
        st.subheader(f"Trimestre {st.session_state.game_manager.current_quarter}")

        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input("Preço do produto", min_value=0, value=100)
            production = st.number_input("Quantidade a produzir", min_value=0, value=1000)
            marketing = st.number_input("Investimento em marketing", min_value=0, value=5000)
        with col2:
            capacity_investment = st.number_input("Investimento em capacidade", min_value=0, value=0)
            research = st.number_input("Investimento em P&D", min_value=0, value=1000)
            donations = st.number_input("Doações", min_value=0, value=0)

        if st.button("Avançar Trimestre"):
            result = st.session_state.game_manager.play_quarter(
                price, production, marketing, capacity_investment, research, donations
            )
            st.write(f"Condição do mercado: {result['market_condition']}")
            st.write(f"Demanda: {result['demand']}")
            st.write(f"Lucro: ${result['profit']}")
            st.write(f"Saldo atual: ${result['balance']}")

if __name__ == "__main__":
    main()
''',
            "pages": {
                "__init__.py": "",
                "dashboard.py": "# Página do painel principal",
                "decisions.py": "# Página para tomada de decisões",
                "reports.py": "# Página de relatórios"
            },
            "components": {
                "__init__.py": "",
                "charts.py": "# Componentes de gráficos",
                "forms.py": "# Componentes de formulários"
            }
        }
    }

    # Arquivos raiz
    root_files = {
        "main.py": '''\
from game_data.company import Company

def main():
    print("Bem-vindo ao Simulador Empresarial!")
    player_company = Company(name="Empresa Teste", initial_balance=10000)
    player_company.set_decisions(35.0, 1000, 5000, 0, 1000, 0)
    demand = 1000
    profit = player_company.calculate_profit(demand)
    print(f"Lucro estimado: ${profit:.2f}")

if __name__ == "__main__":
    main()
''',
        "README.md": '''\
# Simulador Empresarial

## Descrição do Projeto

O Simulador Empresarial é um jogo de simulação inspirado no JA Titan, onde os jogadores assumem o papel de CEOs e gerenciam uma empresa. O objetivo é maximizar o lucro e alcançar a melhor performance no mercado em um período de simulação.

## Como Rodar o Jogo

Execute o seguinte comando no terminal:

```bash
streamlit run frontend/app.py
```
''',
        "requirements.txt": '''\
streamlit==1.22.0
numpy==1.22.4
pandas==1.5.3
plotly==5.14.1
''',
        ".gitignore": '''\
__pycache__/
.vscode/
venv/
*.pyc
'''
    }

    # Função para criar a estrutura de diretórios e arquivos
    def create_structure(base_path, structure):
        for name, content in structure.items():
            if isinstance(content, dict):
                # É um diretório
                dir_path = base_path / name
                dir_path.mkdir(parents=True, exist_ok=True)
                create_structure(dir_path, content)
            else:
                # É um arquivo
                file_path = base_path / name
                create_file(file_path, content)

    # Cria a estrutura do projeto
    create_structure(base_path, structure)

    # Cria os arquivos raiz
    for file_name, content in root_files.items():
        file_path = base_path / file_name
        create_file(file_path, content)

    print(f"Estrutura do projeto criada com sucesso em '{base_dir}'!")

if __name__ == "__main__":
    base_directory = "simulacao_empresarial"
    create_project_structure(base_directory)
