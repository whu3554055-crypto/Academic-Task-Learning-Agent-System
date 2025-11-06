"""
Workflow orchestration for ATLAS multi-agent system.

Creates and manages the coordinated workflow graph for multiple AI agents.
"""

from typing import List, Union, Literal
from langgraph.graph import StateGraph, START, END
from atlas.state import AcademicState
from atlas.coordinator import coordinator_agent, profile_analyzer
from atlas.executor import AgentExecutor


def create_agents_graph(llm) -> StateGraph:
    """
    Creates a coordinated workflow graph for multiple AI agents.
    
    This orchestration system manages parallel execution of three specialized agents:
    - PlannerAgent: Handles scheduling and calendar management
    - NoteWriterAgent: Creates personalized study materials
    - AdvisorAgent: Provides academic guidance and support
    
    The workflow uses a state machine approach with conditional routing based on
    analysis of student needs.
    
    Args:
        llm: Language model instance shared across all agents
        
    Returns:
        Compiled workflow graph with parallel execution paths
    """
    from atlas.agents import PlannerAgent, NoteWriterAgent, AdvisorAgent
    
    # Initialize main workflow state machine
    workflow = StateGraph(AcademicState)

    # Create instances of our specialized agents
    planner_agent = PlannerAgent(llm)
    notewriter_agent = NoteWriterAgent(llm)
    advisor_agent = AdvisorAgent(llm)
    executor = AgentExecutor(llm)

    # === MAIN WORKFLOW NODES ===
    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("profile_analyzer", profile_analyzer)
    workflow.add_node("execute", executor.execute)

    # === PARALLEL EXECUTION ROUTING ===
    def route_to_parallel_agents(state: AcademicState) -> List[str]:
        """
        Determines which agents should process the current request.
        
        Analyzes coordinator's output to route work to appropriate agents.
        Defaults to planner if no specific agents are required.
        
        Args:
            state: Current academic state with coordinator analysis
            
        Returns:
            List of next node names to execute
        """
        analysis = state["results"].get("coordinator_analysis", {})
        required_agents = analysis.get("required_agents", [])
        next_nodes = []

        # Route to appropriate agent entry points based on analysis
        if "PLANNER" in required_agents:
            next_nodes.append("calendar_analyzer")
        if "NOTEWRITER" in required_agents:
            next_nodes.append("notewriter_analyze")
        if "ADVISOR" in required_agents:
            next_nodes.append("advisor_analyze")

        # Default to planner if no specific agents requested
        return next_nodes if next_nodes else ["calendar_analyzer"]

    # === AGENT SUBGRAPH NODES ===
    # Add nodes for Planner agent's workflow
    workflow.add_node("calendar_analyzer", planner_agent.calendar_analyzer)
    workflow.add_node("task_analyzer", planner_agent.task_analyzer)
    workflow.add_node("plan_generator", planner_agent.plan_generator)

    # Add nodes for NoteWriter agent's workflow
    workflow.add_node("notewriter_analyze", notewriter_agent.analyze_learning_style)
    workflow.add_node("notewriter_generate", notewriter_agent.generate_notes)

    # Add nodes for Advisor agent's workflow
    workflow.add_node("advisor_analyze", advisor_agent.analyze_situation)
    workflow.add_node("advisor_generate", advisor_agent.generate_guidance)

    # === WORKFLOW CONNECTIONS ===
    # Main workflow entry
    workflow.add_edge(START, "coordinator")
    workflow.add_edge("coordinator", "profile_analyzer")

    # Connect profile analyzer to potential parallel paths
    workflow.add_conditional_edges(
        "profile_analyzer",
        route_to_parallel_agents,
        ["calendar_analyzer", "notewriter_analyze", "advisor_analyze"]
    )

    # Connect Planner agent's internal workflow
    workflow.add_edge("calendar_analyzer", "task_analyzer")
    workflow.add_edge("task_analyzer", "plan_generator")
    workflow.add_edge("plan_generator", "execute")

    # Connect NoteWriter agent's internal workflow
    workflow.add_edge("notewriter_analyze", "notewriter_generate")
    workflow.add_edge("notewriter_generate", "execute")

    # Connect Advisor agent's internal workflow
    workflow.add_edge("advisor_analyze", "advisor_generate")
    workflow.add_edge("advisor_generate", "execute")

    # === WORKFLOW COMPLETION CHECKING ===
    def should_end(state) -> Union[Literal["coordinator"], Literal[END]]:
        """
        Determines if all required agents have completed their tasks.
        
        Compares the set of completed agent outputs against required agents
        to decide whether to end or continue the workflow.
        
        Args:
            state: Current academic state
            
        Returns:
            Either "coordinator" to continue or END to finish
        """
        analysis = state["results"].get("coordinator_analysis", {})
        executed = set(state["results"].get("agent_outputs", {}).keys())
        required = set(a.lower() for a in analysis.get("required_agents", []))
        return END if required.issubset(executed) else "coordinator"

    # Add conditional loop back to coordinator if needed
    workflow.add_conditional_edges(
        "execute",
        should_end,
        {
            "coordinator": "coordinator",
            END: END
        }
    )

    # Compile and return the complete workflow
    return workflow.compile()
