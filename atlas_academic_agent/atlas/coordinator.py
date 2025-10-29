"""
Coordinator agent for orchestrating multiple academic support agents.
"""

import json
from typing import Dict, List
from atlas.state import AcademicState
from atlas.llm import NeMoLLaMa


# Global LLM instance (will be set by main module)
llm: NeMoLLaMa = None


COORDINATOR_PROMPT = """You are a Coordinator Agent using ReACT framework to orchestrate multiple academic support agents.

        AVAILABLE AGENTS:
        • PLANNER: Handles scheduling and time management
        • NOTEWRITER: Creates study materials and content summaries
        • ADVISOR: Provides personalized academic guidance

        PARALLEL EXECUTION RULES:
        1. Group compatible agents that can run concurrently
        2. Maintain dependencies between agent executions
        3. Coordinate results from parallel executions

        REACT PATTERN:
        Thought: [Analyze request complexity and required support types]
        Action: [Select optimal agent combination]
        Observation: [Evaluate selected agents' capabilities]
        Decision: [Finalize agent deployment plan]

        ANALYSIS POINTS:
        1. Task Complexity and Scope
        2. Time Constraints
        3. Resource Requirements
        4. Learning Style Alignment
        5. Support Type Needed

        CONTEXT:
        Request: {request}
        Student Context: {context}

        FORMAT RESPONSE AS:
        Thought: [Analysis of academic needs and context]
        Action: [Agent selection and grouping strategy]
        Observation: [Expected workflow and dependencies]
        Decision: [Final agent deployment plan with rationale]
        """


async def analyze_context(state: AcademicState) -> Dict:
    """
    Analyzes the academic state context to inform coordinator decision-making.
    
    This function performs comprehensive context analysis by:
    1. Extracting student profile information
    2. Analyzing calendar and task loads
    3. Identifying relevant course context from the latest message
    4. Gathering learning preferences and study patterns
    
    Args:
        state: Current academic state including profile, calendar, and tasks
        
    Returns:
        Structured analysis of the student's context for decision making
    """
    # Extract main data components with safe navigation
    profile = state.get("profile", {})
    calendar = state.get("calendar", {})
    tasks = state.get("tasks", {})

    # Extract course information and match with current request
    courses = profile.get("academic_info", {}).get("current_courses", [])
    current_course = None
    request = state["messages"][-1].content.lower()  # Latest message for context

    # Identify relevant course from request content
    for course in courses:
        if course["name"].lower() in request:
            current_course = course
            break

    # Construct comprehensive context analysis
    return {
        "student": {
            "major": profile.get("personal_info", {}).get("major", "Unknown"),
            "year": profile.get("personal_info", {}).get("academic_year"),
            "learning_style": profile.get("learning_preferences", {}).get("learning_style", {}),
        },
        "course": current_course,
        "upcoming_events": len(calendar.get("events", [])),
        "active_tasks": len(tasks.get("tasks", [])),
        "study_patterns": profile.get("learning_preferences", {}).get("study_patterns", {})
    }


def parse_coordinator_response(response: str) -> Dict:
    """
    Parses LLM coordinator response into structured analysis for agent execution.
    
    This function implements a robust parsing strategy:
    1. Starts with safe default configuration
    2. Analyzes ReACT patterns in the response
    3. Adjusts agent requirements and priorities based on content
    4. Organizes concurrent execution groups
    
    Args:
        response: Raw LLM response text
        
    Returns:
        Structured analysis containing:
        - required_agents: List of agents needed
        - priority: Priority levels for each agent
        - concurrent_groups: Groups of agents that can run together
        - reasoning: Extracted reasoning for decisions
    """
    try:
        # Initialize with safe default configuration
        analysis = {
            "required_agents": ["PLANNER"],
            "priority": {"PLANNER": 1},
            "concurrent_groups": [["PLANNER"]],
            "reasoning": "Default coordination"
        }

        # Parse ReACT patterns for advanced coordination
        if "Thought:" in response and "Decision:" in response:
            # Check for NOTEWRITER requirements
            if "NoteWriter" in response or "note" in response.lower():
                analysis["required_agents"].append("NOTEWRITER")
                analysis["priority"]["NOTEWRITER"] = 2
                # NOTEWRITER can run concurrently with PLANNER
                analysis["concurrent_groups"] = [["PLANNER", "NOTEWRITER"]]

            # Check for ADVISOR requirements
            if "Advisor" in response or "guidance" in response.lower():
                analysis["required_agents"].append("ADVISOR")
                analysis["priority"]["ADVISOR"] = 3
                # ADVISOR typically runs after initial planning

            # Extract and store reasoning from thought section
            thought_section = response.split("Thought:")[1].split("Action:")[0].strip()
            analysis["reasoning"] = thought_section

        return analysis

    except Exception as e:
        print(f"Parse error: {str(e)}")
        # Fallback to safe default configuration
        return {
            "required_agents": ["PLANNER"],
            "priority": {"PLANNER": 1},
            "concurrent_groups": [["PLANNER"]],
            "reasoning": "Fallback due to parse error"
        }


async def coordinator_agent(state: AcademicState) -> Dict:
    """
    Primary coordinator agent that orchestrates multiple academic support agents using ReACT framework.
    
    This agent implements a sophisticated coordination strategy:
    1. Analyzes academic context and student needs
    2. Uses ReACT framework for structured decision making
    3. Coordinates parallel agent execution
    4. Handles fallback scenarios
    
    Args:
        state: Current academic state including messages and context
        
    Returns:
        Coordination analysis including required agents, priorities, and execution groups
    """
    try:
        # Analyze current context and extract latest query
        context = await analyze_context(state)
        query = state["messages"][-1].content

        # Define the ReACT-based coordination prompt
        prompt = COORDINATOR_PROMPT

        # Generate coordination plan using LLM
        response = await llm.agenerate([
            {"role": "system", "content": prompt.format(
                request=query,
                context=json.dumps(context, indent=2)
            )}
        ])

        # Parse response and structure coordination analysis
        analysis = parse_coordinator_response(response)
        return {
            "results": {
                "coordinator_analysis": {
                    "required_agents": analysis.get("required_agents", ["PLANNER"]),
                    "priority": analysis.get("priority", {"PLANNER": 1}),
                    "concurrent_groups": analysis.get("concurrent_groups", [["PLANNER"]]),
                    "reasoning": response
                }
            }
        }

    except Exception as e:
        print(f"Coordinator error: {e}")
        # Fallback to basic planning configuration
        return {
            "results": {
                "coordinator_analysis": {
                    "required_agents": ["PLANNER"],
                    "priority": {"PLANNER": 1},
                    "concurrent_groups": [["PLANNER"]],
                    "reasoning": "Error in coordination. Falling back to planner."
                }
            }
        }


async def profile_analyzer(state: AcademicState) -> Dict:
    """
    Analyzes student profile data to extract and interpret learning preferences.
    
    Args:
        state: Current academic state containing student profile data
        
    Returns:
        Structured analysis results including learning preferences and recommendations
    """
    PROFILE_ANALYZER_PROMPT = """You are a Profile Analysis Agent using the ReACT framework to analyze student profiles.

    OBJECTIVE:
    Analyze the student profile and extract key learning patterns that will impact their academic success.

    REACT PATTERN:
    Thought: Analyze what aspects of the profile need investigation
    Action: Extract specific information from relevant profile sections
    Observation: Note key patterns and implications
    Response: Provide structured analysis

    PROFILE DATA:
    {profile}

    ANALYSIS FRAMEWORK:
    1. Learning Characteristics:
        • Primary learning style
        • Information processing patterns
        • Attention span characteristics

    2. Environmental Factors:
        • Optimal study environment
        • Distraction triggers
        • Productive time periods

    3. Executive Function:
        • Task management patterns
        • Focus duration limits
        • Break requirements

    4. Energy Management:
        • Peak energy periods
        • Recovery patterns
        • Fatigue signals

    FORMAT YOUR RESPONSE AS:
    Thought: [Initial analysis of profile components]
    Action: [Specific areas being examined]
    Observation: [Patterns and insights discovered]
    Analysis Summary: [Structured breakdown of key findings]
    Recommendations: [Specific adaptations needed]
    """
    
    # Extract profile data from state
    profile = state["profile"]

    # Construct message array for LLM interaction
    messages = [
        {"role": "system", "content": PROFILE_ANALYZER_PROMPT},
        {"role": "user", "content": json.dumps(profile)}
    ]

    # Generate analysis using LLM
    response = await llm.agenerate(messages)

    # Format and structure the analysis results
    return {
        "results": {
            "profile_analysis": {
                "analysis": response
            }
        }
    }
