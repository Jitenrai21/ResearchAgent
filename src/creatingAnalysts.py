from src.utils.nodes import create_analysts
from langgraph.graph import START, END, StateGraph
from utils.states import GenerateAnalystState
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

#creating a state graph for the research agent project
builder = StateGraph(GenerateAnalystState)

builder.add_node("create_analysts", create_analysts)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", END)

graph = builder.compile()