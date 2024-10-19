import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

class AccountantAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.2, model="gpt-4o-mini")
        self.prompt = PromptTemplate(
            input_variables=["ledger", "query"],
            template="Você é um contador experiente. Com base no seguinte razão contábil:\n\n{ledger}\n\nPor favor, {query}"
        )
        self.chain = self.prompt | self.llm
        self.ledger = pd.DataFrame(columns=['Date', 'Account', 'Debit', 'Credit', 'Description'])
        self.initialize_accounts()

    def initialize_accounts(self):
        initial_transactions = [
            ('Initial', 'Cash', 100000, 0, 'Initial cash balance'),
            ('Initial', 'Capital', 0, 100000, 'Initial capital')
        ]
        for transaction in initial_transactions:
            self.record_transaction(*transaction)

    def record_transaction(self, date, account, debit, credit, description):
        new_entry = pd.DataFrame({
            'Date': [date],
            'Account': [account],
            'Debit': [debit],
            'Credit': [credit],
            'Description': [description]
        })
        self.ledger = pd.concat([self.ledger, new_entry], ignore_index=True)
        print(f"Transaction recorded: {date}, {account}, Debit: {debit}, Credit: {credit}, {description}")

    def get_account_balance(self, account):
        account_transactions = self.ledger[self.ledger['Account'] == account]
        balance = account_transactions['Debit'].sum() - account_transactions['Credit'].sum()
        return balance

    def generate_income_statement(self):
        sales = abs(self.get_account_balance('Sales'))
        cogs = abs(self.get_account_balance('COGS'))
        gross_margin = sales - cogs
        marketing = abs(self.get_account_balance('Marketing'))
        rd = abs(self.get_account_balance('R&D'))
        donations = abs(self.get_account_balance('Donations'))
        net_profit = gross_margin - marketing - rd - donations

        print(f"Income Statement Debug: Sales={sales}, COGS={cogs}, Marketing={marketing}, R&D={rd}, Donations={donations}")

        return {
            "Sales": sales,
            "Cost of Goods Sold": cogs,
            "Gross Margin": gross_margin,
            "Marketing": marketing,
            "R&D": rd,
            "Charitable Giving": donations,
            "Net Profit": net_profit
        }

    def generate_balance_sheet(self):
        cash = self.get_account_balance('Cash')
        inventory = self.get_account_balance('Inventory')
        capital_investment = self.get_account_balance('Capital Investment')
        total_assets = cash + inventory + capital_investment

        loans = self.get_account_balance('Loans')
        retained_earnings = self.get_account_balance('Retained Earnings')
        capital = abs(self.get_account_balance('Capital'))  # Corrigido para ser positivo
        total_liabilities_equity = loans + retained_earnings + capital

        return {
            "Total Assets": {
                "Cash": cash,
                "Inventory": inventory,
                "Capital Investment": capital_investment
            },
            "Liabilities + Equity": {
                "Loans": loans,
                "Retained Earnings": retained_earnings,
                "Capital": capital
            },
            "Total Assets": total_assets,
            "Total Liabilities + Equity": total_liabilities_equity
        }

    def generate_cash_flow(self):
        beginning_cash = self.get_beginning_cash()
        net_profit = self.generate_income_statement()["Net Profit"]
        depreciation = self.calculate_depreciation()
        capital_investment = abs(self.get_account_balance('Capital Investment'))
        inventory_change = self.calculate_inventory_change()
        loan_changes = self.calculate_loan_changes()
        
        ending_cash = beginning_cash + net_profit + depreciation - capital_investment - inventory_change + loan_changes
        
        return {
            "Beginning Cash": beginning_cash,
            "Net Profit": net_profit,
            "Depreciation": depreciation,
            "Capital Investment": capital_investment,
            "Inventory Change": inventory_change,
            "New Loans/Repayments": loan_changes,
            "Ending Cash": {
                "Available Cash": ending_cash,
                "Available Credit": 100000,  # Valor arbitrário, ajuste conforme necessário
                "Funds Available": ending_cash + 100000
            }
        }

    def generate_production_marketing_report(self):
        # Simulação baseada no cenário econômico e desempenho de vendas
        sales = abs(self.get_account_balance('Sales'))
        production = min(sales, 3000)  # Assumindo capacidade máxima de 3000
        price_per_unit = 100  # Valor arbitrário, ajuste conforme necessário
        cost_per_unit = 10  # Valor arbitrário, ajuste conforme necessário
        
        return {
            "Production": {
                "Production": production,
                "Factory Capacity": 3000,
                "Capacity Utilization": (production / 3000) * 100,
                "Production Cost/Unit": cost_per_unit,
                "Inventory": self.get_account_balance('Inventory'),
                "Employees": 10  # Valor arbitrário, ajuste conforme necessário
            },
            "Marketing": {
                "Orders Received": sales,
                "Sales Made": sales,
                "Unfilled Orders": 0,
                "Price/Unit Sold": price_per_unit,
                "Total Cost/Unit Sold": cost_per_unit,
                "Margin/Unit Sold": price_per_unit - cost_per_unit
            }
        }

    def get_beginning_cash(self):
        initial_cash = self.ledger[self.ledger['Account'] == 'Cash'].iloc[0]['Debit']
        return initial_cash

    def calculate_depreciation(self):
        # Simplificação: assumindo que não há depreciação por enquanto
        return 0

    def calculate_inventory_change(self):
        inventory_transactions = self.ledger[self.ledger['Account'] == 'Inventory']
        inventory_change = inventory_transactions['Debit'].sum() - inventory_transactions['Credit'].sum()
        return inventory_change

    def calculate_loan_changes(self):
        loan_transactions = self.ledger[self.ledger['Account'] == 'Loans']
        loan_changes = loan_transactions['Credit'].sum() - loan_transactions['Debit'].sum()
        return loan_changes

    def print_ledger(self):
        print("Current Ledger:")
        print(self.ledger.to_string())
        print("\nAccount Balances:")
        for account in ['Sales', 'COGS', 'Marketing', 'R&D', 'Donations', 'Cash', 'Inventory', 'Capital']:
            balance = self.get_account_balance(account)
            print(f"{account}: {balance}")

    def generate_financial_statements(self):
        return {
            "Income Statement": self.generate_income_statement(),
            "Balance Sheet": self.generate_balance_sheet(),
            "Cash Flow": self.generate_cash_flow(),
            "Production and Marketing Report": self.generate_production_marketing_report()
        }

    def analyze_financial_position(self):
        query = "Analise a posição financeira da empresa e forneça insights sobre sua saúde financeira."
        return self.chain.invoke({"ledger": str(self.ledger), "query": query})
