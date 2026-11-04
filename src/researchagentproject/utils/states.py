from typing_extensions import TypedDict, NotRequired
from typing import Optional
from objects import Analyst

class GenerateAnalystState(TypedDict):
    topic: str #Research topic for which the analyst is being generated
    max_analysts: int #Maximum number of analysts to generate
    human_analyst_feedback: NotRequired[Optional[str]] #Human feedback on the generated analysts, if any
    analysts = NotRequired[list[Analyst]] #List of generated analysts