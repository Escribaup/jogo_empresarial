import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório pai ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Agora tente importar
try:
    from agents.game_manager_agent import GameManagerAgent
except ImportError as e:
    st.error(f"Erro ao importar GameManagerAgent: {e}")
    st.error(f"PYTHONPATH atual: {sys.path}")
    st.error(f"Conteúdo do diretório agents: {os.listdir(os.path.join(parent_dir, 'agents'))}")
    raise

load_dotenv()

def main():
    st.set_page_config(page_title="Simulador Empresarial", page_icon="🏢", layout="wide")
    st.title("Simulador Empresarial 🏢")

    if 'game_manager' not in st.session_state:
        st.session_state.game_manager = GameManagerAgent()

    st.header("Tome suas decisões para este trimestre")

    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("Preço do produto", min_value=0.0, value=100.0, step=0.1)
        production = st.number_input("Quantidade a produzir", min_value=0, value=1000)
        marketing = st.number_input("Investimento em marketing", min_value=0, value=5000)
    with col2:
        capacity_investment = st.number_input("Investimento em capacidade", min_value=0, value=0)
        research = st.number_input("Investimento em P&D", min_value=0, value=1000)
        donations = st.number_input("Doações", min_value=0, value=0)

    if st.button("Avançar Trimestre"):
        player_decisions = {
            "price": price,
            "production": production,
            "marketing": marketing,
            "capacity_investment": capacity_investment,
            "research": research,
            "donations": donations
        }
        
        try:
            result = st.session_state.game_manager.run_game(player_decisions)
            st.write(result)
            
            # Exibir relatórios financeiros detalhados
            financial_reports = st.session_state.game_manager.df.iloc[-1]['financials']
            
            st.subheader("Demonstração de Resultados")
            st.table(financial_reports["Income Statement"])
            
            st.subheader("Balanço Patrimonial")
            st.table(financial_reports["Balance Sheet"])
            
            st.subheader("Relatório de Produção e Marketing")
            st.table(financial_reports["Production and Marketing Report"])
            
            st.subheader("Fluxo de Caixa")
            st.table(financial_reports["Cash Flow"])
            
            # Exibir análise financeira
            st.subheader("Análise Financeira")
            st.write(st.session_state.game_manager.df.iloc[-1]['analysis'])
            
            # Exibir razão contábil
            st.subheader("Razão Contábil")
            st.dataframe(st.session_state.game_manager.accountant.ledger)
        except Exception as e:
            st.error(f"Ocorreu um erro ao executar o jogo: {str(e)}")
            st.exception(e)

    if hasattr(st.session_state.game_manager, 'df') and not st.session_state.game_manager.df.empty:
        st.subheader("Histórico do Jogo")
        st.dataframe(st.session_state.game_manager.df)

    # Adicione esta seção para mostrar o estado atual do jogo
    if hasattr(st.session_state.game_manager, 'df') and not st.session_state.game_manager.df.empty:
        st.subheader("Estado Atual do Jogo")
        current_state = st.session_state.game_manager.df.iloc[-1]
        st.write(f"Trimestre: {current_state['quarter']}")
        st.write(f"Economia: {current_state['economy']}")
        st.write(f"Competidores: {current_state['competitors']}")
        st.write(f"Finanças: {current_state['financials']}")
        st.write(f"Decisões: {current_state['decisions']}")

    if hasattr(st.session_state.game_manager, 'company_reports'):
        st.subheader("Relatórios Detalhados")
        
        st.write("### Income Statement")
        st.table(st.session_state.game_manager.company_reports.income_statement)
        
        st.write("### Balance Sheet")
        st.table(st.session_state.game_manager.company_reports.balance_sheet)
        
        st.write("### Production Report")
        st.table(st.session_state.game_manager.company_reports.production_report)
        
        st.write("### Marketing Report")
        st.table(st.session_state.game_manager.company_reports.marketing_report)
        
        st.write("### Cash Flow")
        st.table(st.session_state.game_manager.company_reports.cash_flow)

if __name__ == "__main__":
    main()
