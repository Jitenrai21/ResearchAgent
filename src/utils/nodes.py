from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState
from src.utils.models import llm
from src.utils.objects import Analyst, Perspectives
from src.utils.prompts import analyst_instructions
from langchain.messages import SystemMessage, HumanMessage

load_dotenv()  # Load environment variables from .env file

# Creating nodes for the research agent project
def create_analysts(state: GenerateAnalystState):
    """Creates a list of analysts based on the provided state."""
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback", "")

    #Enforce structured output
    structured_llm = llm.with_structured_output(Perspectives)

    # System Message
    system_message = analyst_instructions.format(topic=topic, human_analyst_feedback=human_analyst_feedback, max_analysts=max_analysts)

    # Generate analysts
    analysts = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Please generate the analysts based on the above instructions.")])

    return {'analysts': analysts.analysts}