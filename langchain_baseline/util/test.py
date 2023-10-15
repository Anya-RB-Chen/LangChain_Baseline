from langchain.vectorstores.faiss import FAISS
from config import Config
import pickle

from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI

from util import ringley_user, ringley_data

"""
This is a test file for the agent framework. It is not used in the main program.
"""

config = Config()
llm = OpenAI(temperature=0)

# load vectorstore
with open("embeddings/MASTER_FAQ_EXCEL.pkl", "rb") as f:
    vectorstore = pickle.load(f)

tools = [
    Tool(
        name="User Personal Service",
        func=ringley_user.run,
        description="useful for when you need to answer questions about user's personal services at Ringley. Input should be a fully formed question.",
    ),
    Tool(
        name="Data Retriever",
        func=ringley_data.run,
        description="useful for when you need to answer questions about the articles, blogs or any other information of Ringley. Input should be a fully formed question.",
    ),
]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)