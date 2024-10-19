from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

class CompetitorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")
        self.prompt = PromptTemplate(
            input_variables=["market_conditions"],
            template="Simule as ações dos competidores em um jogo de simulação empresarial. Condições de mercado: {market_conditions}"
        )
        self.chain = self.prompt | self.llm

    def simulate(self, market_conditions):
        return self.chain.invoke({"market_conditions": market_conditions})

    def simulate(self, df):
        # Implementação simplificada
        return "Competidores mantêm suas estratégias"
