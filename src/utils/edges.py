from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState
from typing import Literal
from langgraph.graph import END

load_dotenv()  # Load environment variables from .env file

def should_continue(state: GenerateAnalystState) -> Literal["create_analysts", END]:
    """Returns next  node to be executed"""
    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        return "create_analysts"  # Regenerate analysts based on feedback

    return END