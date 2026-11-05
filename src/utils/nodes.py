from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState, InterviewState
from src.utils.models import llm
from src.utils.objects import Analyst, Perspectives, SearchQuery
from src.utils.prompts import analyst_instructions, question_instructions, search_instruction, answer_instructions, section_writer_instructions
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string

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

# Questions for interview loop
def generate_question(state: InterviewState):
    """Node to generate interview questions"""

    # get state analyst
    analyst = state["analyst"]
    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    messages = state["messages"]

    #generate question
    system_message = question_instructions.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)]+messages)

    return {"messages": [question]}

def search_web(state: InterviewState):
    """Retrieve docs from the web"""

    #search query
    structured_llm = llm.with_structured_output(SearchQuery, method="json_schema")

    #search instruction
    search_instruction_sys_message = SystemMessage(content=search_instruction)
    tavily_search = TavilySearch(max_results=3)

    search_query = structured_llm.invoke(
        [search_instruction_sys_message]
        + state["messages"]
        + [HumanMessage(content="Generate the search query JSON now.")]
    )

    #search
    data = tavily_search.invoke({"query": search_query.search_query})
    search_docs = data.get("results", data)

    #format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def search_web2(state: InterviewState):
    """Retrieve docs from the web"""

    #search query
    structured_llm = llm.with_structured_output(SearchQuery, method="json_schema")

    #search instruction
    search_instruction_sys_message = SystemMessage(content=search_instruction)
    tavily_search = TavilySearch(max_results=3)

    search_query = structured_llm.invoke(
        [search_instruction_sys_message]
        + state["messages"]
        + [HumanMessage(content="Generate the search query JSON now.")]
    )

    #search
    data = tavily_search.invoke({"query": search_query.search_query})
    search_docs = data.get("results", data)

    #format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def generate_answer(state: InterviewState):
    """Node to answer the question"""

    #get state
    analyst = state['analyst']
    messages = state['messages']
    context = state['context']

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    # answer question
    system_message = answer_instructions.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)]+messages)

    # naming the message as coming from the expert
    answer.name = "expert"

    #append to the state
    return {"messages": [answer]}

def save_interview(state: InterviewState):
    """Save interview"""

    messages = state["messages"]

    interview = get_buffer_string(messages)

    return {"interview": interview}

def write_section(state: InterviewState):
    """Node to answer a question"""

    interview = state['interview']
    context = state["context"]
    analyst = state["analyst"]

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    system_message = section_writer_instructions.format(focus=analyst.description)
    section = llm.invoke([SystemMessage(content=system_message)]+
                         [HumanMessage(content=f"Use this source to write your section: {context}")])
    
    return {"sections": [section.content]}