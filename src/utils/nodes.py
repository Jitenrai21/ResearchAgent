from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState
from src.utils.models import llm
from src.utils.objects import Analyst, Perspectives
from src.utils.prompts import analyst_instructions
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt

load_dotenv()  # Load environment variables from .env file

# Creating nodes for the research agent project
def create_analysts(state: GenerateAnalystState):

    """Creates a list of analysts based on the provided state."""
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback", "")

    #Enforce structured output via JSON schema (avoids Groq tool-call param validation)
    structured_llm = llm.with_structured_output(Perspectives, method="json_schema")

    # System Message
    system_message = analyst_instructions.format(topic=topic, human_analyst_feedback=human_analyst_feedback, max_analysts=max_analysts)

    # Generate analysts
    analysts = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Please generate the analysts based on the above instructions.")])

    return {'analysts': analysts.analysts}

# Human Feedback Node
def human_feedback(state: GenerateAnalystState):
    """This is where the human gives feedback about the analysts generated."""

    feedback =  interrupt({
        "question": "Are these analysts good to go?",
        "analysts": [
            analyst.model_dump() if hasattr(analyst, "model_dump") else analyst for analyst in state.get("analysts", [])
        ],
        "instructions": "Return Feedback to regenerate analysts or return empty/perfect/continue/okay to approve and continue with the graph execution."
    })

    if feedback is None:
        return {"human_analyst_feedback": None}  # No feedback provided

    if isinstance(feedback, str):
        feedback = feedback.strip()

        if feedback == "":
            return {"human_analyst_feedback": None}  # No feedback provided

        if feedback.lower() in {"empty", "perfect", "continue", "okay"}:
            return {"human_analyst_feedback": None}  # Feedback indicates approval no changes actually

        return {"human_analyst_feedback": feedback}  # Return the feedback for further processing

    return {"human_analyst_feedback": None} 

