from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

class DecisionAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")
        self.prompt = PromptTemplate(
            input_variables=["game_state"],
            template="Com base no estado atual do jogo: {game_state}, sugira decisões estratégicas para o próximo trimestre."
        )
        self.chain = self.prompt | self.llm

    def suggest(self, game_state):
        return self.chain.invoke({"game_state": str(game_state)})
