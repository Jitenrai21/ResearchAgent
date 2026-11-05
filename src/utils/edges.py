from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState, InterviewState
from typing import Literal
from langgraph.graph import END
from langchain.messages import AIMessage

load_dotenv()  # Load environment variables from .env file

def should_continue(state: GenerateAnalystState) -> Literal["create_analysts", END]:
    """Returns next  node to be executed"""
    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        return "create_analysts"  # Regenerate analysts based on feedback

    return END

def route_messages(state: InterviewState, name: str="expert"):
    """Route between question and answer"""

    # Get messages
    messages = state["messages"]
    max_num_turns = state.get("max_num_turns", 2)

    # Check the number of expert answers
    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == name])

    if num_responses >= max_num_turns:
        return "save_interview"

    return "ask_question"
