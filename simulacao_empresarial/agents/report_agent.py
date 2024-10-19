from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

class ReportAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
        self.prompt = PromptTemplate(
            input_variables=["game_data"],
            template="Gere um relatório financeiro e de mercado com base nos seguintes dados do jogo: {game_data}"
        )
        self.chain = self.prompt | self.llm

    def generate(self, game_data):
        return self.chain.invoke({"game_data": str(game_data)})
