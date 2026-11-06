from src.utils.nodes import *
from src.utils.states import ResearchGraphState
from langgraph.graph import StateGraph, START, END
from src.answeringQuestion import interview_builder
from src.utils.edges import initiate_all_interviews

# Adding nodes and edges
builder = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_builder.compile())
builder.add_node("write_report", write_report)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

# Flow
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", initiate_all_interviews, ["create_analysts", "conduct_interview"])
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge(["write_introduction", "write_report", "write_conclusion"], "finalize_report")
builder.add_edge("finalize_report", END)

# Compile
graph = builder.compile()