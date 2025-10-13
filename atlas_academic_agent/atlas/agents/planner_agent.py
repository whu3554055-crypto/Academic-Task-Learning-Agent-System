"""
Planner Agent for academic scheduling and time management.
"""

import json
from datetime import datetime, timedelta, timezone
from typing import Dict
from langgraph.graph import StateGraph, START, END
from atlas.state import AcademicState
from atlas.agents.base_agent import ReActAgent


class PlannerAgent(ReActAgent):
    """
    Planner agent with subgraph workflow for scheduling and time management.
    
    This agent specializes in:
    - Calendar analysis and conflict detection
    - Task prioritization and scheduling
    - Study plan generation considering learning styles
    - ADHD-optimized scheduling strategies
    
    The workflow consists of three stages:
    1. Calendar analysis (calendar_analyzer)
    2. Task analysis (task_analyzer)
    3. Plan generation (plan_generator)
    """

    def __init__(self, llm):
        """
        Initialize PlannerAgent with LLM and example scenarios.
        
        Args:
            llm: Language model instance for text generation
        """
        super().__init__(llm)
        self.llm = llm
        # Load example scenarios to help guide the AI's responses
        self.few_shot_examples = self._initialize_fewshots()
        # Create the workflow structure
        self.workflow = self.create_subgraph()

    def _initialize_fewshots(self):
        """
        Define example scenarios to help the AI understand how to handle different situations.
        
        Each example shows:
        - Input: The student's request
        - Thought: The analysis process
        - Action: What needs to be done
        - Observation: What was found
        - Plan: The detailed solution
        
        Returns:
            List of few-shot examples
        """
        return [
            {
                "input": "Help with exam prep while managing ADHD and football",
                "thought": "Need to check calendar conflicts and energy patterns",
                "action": "search_calendar",
                "observation": "Football match at 6PM, exam tomorrow 9AM",
                "plan": """ADHD-OPTIMIZED SCHEDULE:
                    PRE-FOOTBALL (2PM-5PM):
                    - 3x20min study sprints
                    - Movement breaks
                    - Quick rewards after each sprint

                    FOOTBALL MATCH (6PM-8PM):
                    - Use as dopamine reset
                    - Formula review during breaks

                    POST-MATCH (9PM-12AM):
                    - Environment: Café noise
                    - 15/5 study/break cycles
                    - Location changes hourly

                    EMERGENCY PROTOCOLS:
                    - Focus lost → jumping jacks
                    - Overwhelmed → room change
                    - Brain fog → cold shower"""
            },
            {
                "input": "Struggling with multiple deadlines",
                "thought": "Check task priorities and performance issues",
                "action": "analyze_tasks",
                "observation": "3 assignments due, lowest grade in Calculus",
                "plan": """PRIORITY SCHEDULE:
                    HIGH-FOCUS SLOTS:
                    - Morning: Calculus practice
                    - Post-workout: Assignments
                    - Night: Quick reviews

                    ADHD MANAGEMENT:
                    - Task timer challenges
                    - Reward system per completion
                    - Study buddy accountability"""
            }
        ]

    def create_subgraph(self) -> StateGraph:
        """
        Create a workflow graph that defines how the planner processes requests.
        
        Workflow:
        1. First analyzes calendar (calendar_analyzer)
        2. Then analyzes tasks (task_analyzer)
        3. Finally generates a plan (plan_generator)
        
        Returns:
            Compiled StateGraph ready for execution
        """
        # Initialize a new graph using our AcademicState structure
        subgraph = StateGraph(AcademicState)

        # Add each processing step as a node in our graph
        subgraph.add_node("calendar_analyzer", self.calendar_analyzer)
        subgraph.add_node("task_analyzer", self.task_analyzer)
        subgraph.add_node("plan_generator", self.plan_generator)

        # Connect the nodes in the order they should execute
        subgraph.add_edge("calendar_analyzer", "task_analyzer")
        subgraph.add_edge("task_analyzer", "plan_generator")

        # Set where the workflow begins
        subgraph.set_entry_point("calendar_analyzer")

        # Prepare the graph for use
        return subgraph.compile()

    async def calendar_analyzer(self, state: AcademicState) -> AcademicState:
        """
        Analyze the student's calendar to find available study times, conflicts, and energy patterns.
        
        Args:
            state: Current academic state
            
        Returns:
            Updated state with calendar analysis results
        """
        # Get calendar events for the next 7 days
        events = state["calendar"].get("events", [])
        now = datetime.now(timezone.utc)
        future = now + timedelta(days=7)

        # Filter to only include upcoming events
        filtered_events = [
            event for event in events
            if now <= datetime.fromisoformat(event["start"]["dateTime"]) <= future
        ]

        # Create prompt for the AI to analyze the calendar
        prompt = """Analyze calendar events and identify:
        Events: {events}

        Focus on:
        - Available time blocks
        - Energy impact of activities
        - Potential conflicts
        - Recovery periods
        - Study opportunity windows
        - Activity patterns
        - Schedule optimization
        """

        # Ask AI to analyze the calendar
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(filtered_events)}
        ]

        response = await self.llm.agenerate(messages)

        # Return the analysis results
        return {
            "results": {
                "calendar_analysis": {
                    "analysis": response
                }
            }
        }

    async def task_analyzer(self, state: AcademicState) -> AcademicState:
        """
        Analyze tasks to determine priority order, time needed, and best approach.
        
        Args:
            state: Current academic state
            
        Returns:
            Updated state with task analysis results
        """
        tasks = state["tasks"].get("tasks", [])

        # Create prompt for AI to analyze tasks
        prompt = """Analyze tasks and create priority structure:
        Tasks: {tasks}

        Consider:
        - Urgency levels
        - Task complexity
        - Energy requirements
        - Dependencies
        - Required focus levels
        - Time estimations
        - Learning objectives
        - Success criteria
        """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(tasks)}
        ]

        response = await self.llm.agenerate(messages)

        return {
            "results": {
                "task_analysis": {
                    "analysis": response
                }
            }
        }

    async def plan_generator(self, state: AcademicState) -> AcademicState:
        """
        Create a comprehensive study plan by combining profile, calendar, and task analyses.
        
        Args:
            state: Current academic state with all analyses completed
            
        Returns:
            Updated state with final study plan
        """
        # Gather all previous analyses
        profile_analysis = state["results"]["profile_analysis"]
        calendar_analysis = state["results"]["calendar_analysis"]
        task_analysis = state["results"]["task_analysis"]

        # Create detailed prompt for AI to generate plan
        prompt = f"""AI Planning Assistant: Create focused study plan using ReACT framework.

          INPUT CONTEXT:
          - Profile Analysis: {profile_analysis}
          - Calendar Analysis: {calendar_analysis}
          - Task Analysis: {task_analysis}

          EXAMPLES:
          {json.dumps(self.few_shot_examples, indent=2)}

          INSTRUCTIONS:
          1. Follow ReACT pattern:
            Thought: Analyze situation and needs
            Action: Consider all analyses
            Observation: Synthesize findings
            Plan: Create structured plan

          2. Address:
            - ADHD management strategies
            - Energy level optimization
            - Task chunking methods
            - Focus period scheduling
            - Environment switching tactics
            - Recovery period planning
            - Social/sport activity balance

          3. Include:
            - Emergency protocols
            - Backup strategies
            - Quick wins
            - Reward system
            - Progress tracking
            - Adjustment triggers

          Pls act as an intelligent tool to help the students reach their goals or overcome struggles and answer with informal words.

          FORMAT:
          Thought: [reasoning and situation analysis]
          Action: [synthesis approach]
          Observation: [key findings]
          Plan: [actionable steps and structural schedule]
          """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": state["messages"][-1].content}
        ]
        # temperature is like a randomness of LLM response, 0.5 is in the middle
        response = await self.llm.agenerate(messages, temperature=0.5)

        return {
            "results": {
                "final_plan": {
                    "plan": response
                }
            }
        }

    async def __call__(self, state: AcademicState) -> Dict:
        """
        Main execution method that runs the entire planning workflow.
        
        Workflow:
        1. Analyze calendar
        2. Analyze tasks
        3. Generate plan
        
        Args:
            state: Initial academic state
            
        Returns:
            Dictionary containing generated plan or error message
        """
        try:
            final_state = await self.workflow.ainvoke(state)
            return {"plan": final_state["results"].get("final_plan")}
        except Exception as e:
            return {"plan": "Error generating plan. Please try again."}
