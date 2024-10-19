from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class EconomyAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")  # ou "gpt-4" se tiver acesso
        self.prompt = ChatPromptTemplate.from_template(
            "Simule a economia para um jogo de simulação empresarial. "
            "Forneça dados sobre PIB, inflação, taxa de juros e desemprego. "
            "Histórico: {history}"
        )

    def simulate(self, df):
        # Implementação simplificada
        return "Economia estável"
