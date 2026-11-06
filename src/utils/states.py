from typing_extensions import TypedDict, NotRequired, Annotated
from typing import Optional, List
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
import operator

class GenerateAnalystState(TypedDict):
    topic: str #Research topic for which the analyst is being generated
    max_analysts: int #Maximum number of analysts to generate
    human_analyst_feedback: NotRequired[Optional[str]] #Human feedback on the generated analysts, if any
    analysts: NotRequired[list[Analyst]] #List of generated analysts

class InterviewState(MessagesState):
    max_num_turns: int # turns of conversation
    context: Annotated[list, operator.add] # source of docs
    analyst: Analyst # my analyst   
    interview: str # interview transcript
    sections: list # final key we duplicate in outer state for Send() api

class ResearchGraphState(TypedDict):
    topic: str # Research Topic
    max_analysts: int # number of analysts
    human_analyst_feedback: NotRequired[Optional[str]]
    analysts: List[Analyst] # Analysts asking questions
    sections: Annotated[list, operator.add] # Send() API key
    introduction: str # Introduction for the final report
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Final Report
