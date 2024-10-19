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
