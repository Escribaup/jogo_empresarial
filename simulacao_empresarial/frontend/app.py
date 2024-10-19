import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.game_manager_agent import GameManagerAgent

load_dotenv()

def simplify_data(data):
    if isinstance(data, dict):
        return {k: simplify_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [simplify_data(item) for item in data]
    elif hasattr(data, '__dict__'):
        return simplify_data(data.__dict__)
    else:
        return str(data)

def format_number(value):
    """
    Formata o número com ',' para decimais e '.' para milhar, sem sinal negativo.
    """
    return f"{abs(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def display_financial_reports(financial_reports):
    st.subheader("Demonstração de Resultados")
    income_statement = financial_reports.get("Income Statement", {})
    income_data = [(k, format_number(v)) for k, v in income_statement.items()]
    st.table(pd.DataFrame(income_data, columns=["Item", "Valor"]))

    st.subheader("Balanço Patrimonial")
    balance_sheet = financial_reports.get("Balance Sheet", {})
    
    if isinstance(balance_sheet, dict):
        assets = balance_sheet.get("Total Assets", {})
        liabilities_equity = balance_sheet.get("Liabilities + Equity", {})
        
        if isinstance(assets, dict) and isinstance(liabilities_equity, dict):
            balance_sheet_data = [
                ("Ativos Totais", ""),
                ("  Cash (Caixa)", format_number(assets.get("Cash", 0))),
                ("  Inventory (Inventário)", format_number(assets.get("Inventory", 0))),
                ("  Capital Invest. (Investimento de Capital)", format_number(assets.get("Capital Investment", 0))),
                ("Total Ativos", format_number(sum(assets.values()))),
                ("", ""),
                ("Passivos + Patrimônio", ""),
                ("  Loans (Empréstimos)", format_number(liabilities_equity.get("Loans", 0))),
                ("  Ret. Earnings (Lucros Retidos)", format_number(liabilities_equity.get("Retained Earnings", 0))),
                ("  Capital", format_number(liabilities_equity.get("Capital", 0))),
                ("Total Passivos + Patrimônio", format_number(sum(liabilities_equity.values())))
            ]
        else:
            balance_sheet_data = [("Dados do Balanço Patrimonial não disponíveis no formato esperado", "")]
    else:
        balance_sheet_data = [("Balanço Patrimonial não disponível", "")]
    
    st.table(pd.DataFrame(balance_sheet_data, columns=["Item", "Valor"]))

    st.subheader("Relatório de Produção e Marketing")
    production_marketing = financial_reports.get("Production and Marketing Report", {})
    if isinstance(production_marketing, dict):
        production_data = [(k, format_number(v) if isinstance(v, (int, float)) else v) 
                           for k, v in production_marketing.get("Production", {}).items()]
        marketing_data = [(k, format_number(v) if isinstance(v, (int, float)) else v) 
                          for k, v in production_marketing.get("Marketing", {}).items()]
        
        st.write("Produção")
        st.table(pd.DataFrame(production_data, columns=["Item", "Valor"]))
        st.write("Marketing")
        st.table(pd.DataFrame(marketing_data, columns=["Item", "Valor"]))
    else:
        st.write("Dados de Produção e Marketing não disponíveis")

    st.subheader("Fluxo de Caixa")
    cash_flow = financial_reports.get("Cash Flow", {})
    if isinstance(cash_flow, dict):
        ending_cash = cash_flow.get("Ending Cash", {})
        if isinstance(ending_cash, dict):
            cash_flow_data = [
                ("Beginning Cash (Caixa Inicial)", format_number(cash_flow.get("Beginning Cash", 0))),
                ("Net Profit (Lucro Líquido)", format_number(cash_flow.get("Net Profit", 0))),
                ("Depreciation (Depreciação)", format_number(cash_flow.get("Depreciation", 0))),
                ("Capital Investment (Investimento de Capital)", format_number(cash_flow.get("Capital Investment", 0))),
                ("Inventory Change (Mudança no Inventário)", format_number(cash_flow.get("Inventory Change", 0))),
                ("New Loans/Repayments (Novos Empréstimos/Amortizações)", format_number(cash_flow.get("New Loans/Repayments", 0))),
                ("Ending Cash (Caixa Final)", ""),
                ("  Available Cash (Caixa Disponível)", format_number(ending_cash.get("Available Cash", 0))),
                ("  Available Credit (Crédito Disponível)", format_number(ending_cash.get("Available Credit", 0))),
                ("  Funds Available (Fundos Disponíveis)", format_number(ending_cash.get("Funds Available", 0)))
            ]
        else:
            cash_flow_data = [("Dados detalhados do Fluxo de Caixa não disponíveis", "")]
    else:
        cash_flow_data = [("Fluxo de Caixa não disponível", "")]
    
    st.table(pd.DataFrame(cash_flow_data, columns=["Item", "Valor"]))

def main():
    st.set_page_config(layout="wide")
    st.title("Simulação Empresarial")

    # Inicializar variáveis de sessão
    if 'game_manager' not in st.session_state:
        st.session_state.game_manager = GameManagerAgent()

    # Inicializar variáveis de decisão do jogador
    if 'production' not in st.session_state:
        st.session_state.production = 0
    if 'price' not in st.session_state:
        st.session_state.price = 0
    if 'marketing' not in st.session_state:
        st.session_state.marketing = 0
    if 'research_development' not in st.session_state:
        st.session_state.research_development = 0
    if 'charitable_giving' not in st.session_state:
        st.session_state.charitable_giving = 0

    # Barra lateral para decisões do jogador
    st.sidebar.header("Decisões do Jogador")
    st.session_state.production = st.sidebar.number_input("Produção", min_value=0, value=st.session_state.production)
    st.session_state.price = st.sidebar.number_input("Preço", min_value=0.0, value=float(st.session_state.price), step=0.01)
    st.session_state.marketing = st.sidebar.number_input("Marketing", min_value=0, value=st.session_state.marketing)
    st.session_state.research_development = st.sidebar.number_input("Pesquisa e Desenvolvimento", min_value=0, value=st.session_state.research_development)
    st.session_state.charitable_giving = st.sidebar.number_input("Doações", min_value=0, value=st.session_state.charitable_giving)

    if st.sidebar.button("Avançar Trimestre"):
        player_decisions = {
            'production': st.session_state.production,
            'price': st.session_state.price,
            'marketing': st.session_state.marketing,
            'research_development': st.session_state.research_development,
            'charitable_giving': st.session_state.charitable_giving
        }
        game_state = st.session_state.game_manager.run_game(player_decisions)
        financial_reports = game_state['financials']

        # Exibir relatórios financeiros
        st.header("Relatórios Financeiros")
        display_financial_reports(financial_reports)

        # Exibir análise financeira
        st.header("Análise Financeira")
        st.write(game_state['analysis'])

        # Exibir dados da economia
        st.header("Dados da Economia")
        st.write(game_state['economy'])

        # Exibir dados dos competidores
        st.header("Dados dos Competidores")
        st.write(game_state['competitors'])

if __name__ == "__main__":
    main()
