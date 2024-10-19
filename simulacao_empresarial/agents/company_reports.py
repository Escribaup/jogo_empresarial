class CompanyReports:
    def __init__(self):
        self.income_statement = {
            "Sales": 0,
            "Cost of Goods Sold": 0,
            "Gross Margin": 0,
            "Marketing": 0,
            "Depreciation": 0,
            "R&D": 0,
            "Layoff Charge": 0,
            "Inventory Charge": 0,
            "Interest": 0,
            "Profit Before Tax": 0,
            "Tax": 0,
            "Charitable Giving": 0,
            "Net Profit": 0
        }
        
        self.balance_sheet = {
            "Total Assets": {
                "Cash": 0,
                "Inventory": 0,
                "Capital Investment": 0
            },
            "Liabilities + Equity": {
                "Loans": 0,
                "Retained Earnings": 0,
                "Capital": 0
            }
        }
        
        self.production_report = {
            "Production": 0,
            "Factory Capacity": 0,
            "Capacity Utilization": 0,
            "Production Cost/Unit": 0,
            "Inventory": 0,
            "Employees": 0
        }
        
        self.marketing_report = {
            "Orders Received": 0,
            "Sales Made": 0,
            "Unfilled Orders": 0,
            "Price/Unit Sold": 0,
            "Total Cost/Unit Sold": 0,
            "Margin/Unit Sold": 0
        }
        
        self.cash_flow = {
            "Beginning Cash": 0,
            "Net Profit": 0,
            "Depreciation": 0,
            "Capital Investment": 0,
            "Inventory Change": 0,
            "New Loans/Repayments": 0,
            "Ending Cash": {
                "Available Cash": 0,
                "Available Credit": 0,
                "Funds Available": 0
            }
        }

    def update_reports(self, game_state, player_decisions):
        # Aqui implementaremos a lógica para atualizar todos os relatórios
        # com base no estado atual do jogo e nas decisões do jogador
        pass

    def generate_reports_summary(self):
        # Aqui geraremos um resumo textual dos relatórios para apresentação
        pass
