"""
Base ReAct agent implementation for ATLAS system.

ReACT (Reasoning and Acting) framework enables LLMs to approach complex tasks
by breaking them down into iterative reasoning and action steps.
"""

from typing import Dict, List, Optional
from atlas.state import AcademicState


class ReActAgent:
    """
    Base class for ReACT-based agents implementing reasoning and action capabilities.

    ReACT Framework:
        1. (Re)act: Take an action based on observations and tools
        2. (Re)ason: Think about what to do next
        3. (Re)flect: Learn from the outcome

    Example Flow:
        - Thought: Need to check student's schedule for study time
        - Action: search_calendar
        - Observation: Found 2 free hours tomorrow morning
        - Thought: Student prefers morning study, this is optimal
        - Action: analyze_tasks
        - Observation: Has 3 pending assignments
        - Plan: Schedule morning study session for highest priority task

    Features:
        - Tool management for specific actions
        - Few-shot learning examples
        - Structured thought process
        - Action execution framework

    Attributes:
        llm: Language model instance for agent operations
        few_shot_examples: Storage for examples to guide the agent
        tools: Dictionary of available tools with their corresponding methods
    """

    def __init__(self, llm):
        """
        Initialize the ReActAgent with language model and available tools.

        Args:
            llm: Language model instance for agent operations
        """
        self.llm = llm
        # Storage for few-shot examples to guide the agent
        self.few_shot_examples = []

        # Dictionary of available tools with their corresponding methods
        self.tools = {
            "search_calendar": self.search_calendar,
            "analyze_tasks": self.analyze_tasks,
            "check_learning_style": self.check_learning_style,
            "check_performance": self.check_performance
        }

    async def search_calendar(self, state: AcademicState) -> List[Dict]:
        """
        Search for upcoming calendar events.

        Args:
            state: Current academic state

        Returns:
            List of upcoming calendar events
        """
        from datetime import datetime, timezone
        
        # Get events from calendar or empty list if none exist
        events = state["calendar"].get("events", [])
        # Get current time in UTC
        now = datetime.now(timezone.utc)
        # Filter and return only future events
        return [e for e in events if datetime.fromisoformat(e["start"]["dateTime"]) > now]

    async def analyze_tasks(self, state: AcademicState) -> List[Dict]:
        """
        Analyze academic tasks from the current state.

        Args:
            state: Current academic state

        Returns:
            List of academic tasks
        """
        # Return tasks or empty list if none exist
        return state["tasks"].get("tasks", [])

    async def check_learning_style(self, state: AcademicState) -> AcademicState:
        """
        Retrieve student's learning style and study patterns.

        Args:
            state: Current academic state

        Returns:
            Updated state with learning style analysis
        """
        # Get user profile from state
        profile = state["profile"]

        # Get learning preferences
        learning_data = {
            "style": profile.get("learning_preferences", {}).get("learning_style", {}),
            "patterns": profile.get("learning_preferences", {}).get("study_patterns", {})
        }

        # Add to results in state
        if "results" not in state:
            state["results"] = {}
        state["results"]["learning_analysis"] = learning_data

        return state

    async def check_performance(self, state: AcademicState) -> AcademicState:
        """
        Check current academic performance across courses.

        Args:
            state: Current academic state

        Returns:
            Updated state with performance analysis
        """
        # Get user profile from state
        profile = state["profile"]

        # Get course information
        courses = profile.get("academic_info", {}).get("current_courses", [])

        # Add to results in state
        if "results" not in state:
            state["results"] = {}
        state["results"]["performance_analysis"] = {"courses": courses}

        return state
