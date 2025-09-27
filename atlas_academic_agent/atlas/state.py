"""
State definitions and data models for the ATLAS academic agent system.
"""

from typing import TypedDict, List, Dict, Any, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


def dict_reducer(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries recursively.

    Example:
        dict1 = {"a": {"x": 1}, "b": 2}
        dict2 = {"a": {"y": 2}, "c": 3}
        result = {"a": {"x": 1, "y": 2}, "b": 2, "c": 3}

    Args:
        dict1: First dictionary
        dict2: Second dictionary to merge

    Returns:
        Merged dictionary
    """
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = dict_reducer(merged[key], value)
        else:
            merged[key] = value
    return merged


class AcademicState(TypedDict):
    """
    Master state container for the academic assistance system.

    Attributes:
        messages: Conversation history with accumulated messages
        profile: Student information (merged using dict_reducer)
        calendar: Scheduled events (merged using dict_reducer)
        tasks: To-do items and assignments (merged using dict_reducer)
        results: Operation outputs from agents (merged using dict_reducer)
    """
    messages: Annotated[List[BaseMessage], add_messages]
    profile: Annotated[Dict, dict_reducer]
    calendar: Annotated[Dict, dict_reducer]
    tasks: Annotated[Dict, dict_reducer]
    results: Annotated[Dict[str, Any], dict_reducer]


# Pydantic models for agent actions and outputs
from pydantic import BaseModel


class AgentAction(BaseModel):
    """
    Model representing an agent's action decision.

    Attributes:
        action: The specific action to be performed
        thought: The reasoning process behind the action choice
        tool: The specific tool to be used for the action (optional)
        action_input: Input parameters for the action (optional)

    Example:
        >>> action = AgentAction(
        ...     action="search_calendar",
        ...     thought="Need to check schedule conflicts",
        ...     tool="calendar_search",
        ...     action_input={"date_range": "next_week"}
        ... )
    """
    action: str
    thought: str
    tool: Optional[str] = None
    action_input: Optional[Dict] = None


class AgentOutput(BaseModel):
    """
    Model representing the output from an agent's action.

    Attributes:
        observation: The result or observation from executing the action
        output: Structured output data from the action

    Example:
        >>> output = AgentOutput(
        ...     observation="Found 3 free time slots next week",
        ...     output={
        ...         "free_slots": ["Mon 2PM", "Wed 10AM", "Fri 3PM"],
        ...         "conflicts": []
        ...     }
        ... )
    """
    observation: str
    output: Dict
