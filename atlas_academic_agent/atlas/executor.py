"""
Agent Executor for orchestrating concurrent execution of multiple AI agents.
"""

import asyncio
from typing import Dict
from atlas.state import AcademicState


class AgentExecutor:
    """
    Orchestrates the concurrent execution of multiple specialized AI agents.
    
    This class implements a sophisticated execution pattern that allows multiple AI agents
    to work together, either sequentially or concurrently, based on a coordination analysis.
    It handles agent initialization, concurrent execution, error handling, and fallback strategies.
    
    Attributes:
        llm: Language model instance used by all agents
        agents: Dictionary of specialized agent instances
    """

    def __init__(self, llm):
        """
        Initialize the executor with a language model and create agent instances.
        
        Args:
            llm: Language model instance to be used by all agents
            
        Implementation Note:
            - Creates a dictionary of specialized agents, each initialized with the same LLM
            - Supports multiple agent types: PLANNER (default), NOTEWRITER, and ADVISOR
            - Agents are instantiated once and reused across executions
        """
        from atlas.agents import PlannerAgent, NoteWriterAgent, AdvisorAgent
        
        self.llm = llm
        self.agents = {
            "PLANNER": PlannerAgent(llm),
            "NOTEWRITER": NoteWriterAgent(llm),
            "ADVISOR": AdvisorAgent(llm)
        }

    async def execute(self, state: AcademicState) -> Dict:
        """
        Orchestrates concurrent execution of multiple AI agents based on analysis results.
        
        This method implements a sophisticated execution pattern:
        1. Reads coordination analysis to determine required agents
        2. Groups agents for concurrent execution
        3. Executes agent groups in parallel
        4. Handles failures gracefully with fallback mechanisms
        
        Args:
            state: Current academic state containing analysis results
            
        Returns:
            Consolidated results from all executed agents
            
        Implementation Details:
        ---------------------
        1. Analysis Interpretation:
           - Extracts coordination analysis from state
           - Determines required agents and their concurrent execution groups

        2. Concurrent Execution Pattern:
           - Processes agents in groups that can run in parallel
           - Uses asyncio.gather() for concurrent execution within each group
           - Only executes agents that are both required and available

        3. Result Management:
           - Collects and processes results from each concurrent group
           - Filters out failed executions (exceptions)
           - Formats successful results into a structured output

        4. Fallback Mechanisms:
           - If no results are gathered, falls back to PLANNER agent
           - Provides emergency fallback plan in case of complete failure
        
        Error Handling:
        --------------
        - Catches and handles exceptions at multiple levels:
          * Individual agent execution failures don't affect other agents
          * System-level failures trigger emergency fallback
        - Maintains system stability through graceful degradation
        """
        try:
            # Extract coordination analysis from state
            analysis = state["results"].get("coordinator_analysis", {})

            # Determine execution requirements
            required_agents = analysis.get("required_agents", ["PLANNER"])
            concurrent_groups = analysis.get("concurrent_groups", [])

            # Initialize results container
            results = {}

            # Process each concurrent group sequentially
            for group in concurrent_groups:
                # Prepare concurrent tasks for current group
                tasks = []
                for agent_name in group:
                    # Validate agent availability and requirement
                    if agent_name in required_agents and agent_name in self.agents:
                        tasks.append(self.agents[agent_name](state))

                # Execute group tasks concurrently if any exist
                if tasks:
                    # Gather results from concurrent execution
                    group_results = await asyncio.gather(*tasks, return_exceptions=True)

                    # Process successful results only
                    for agent_name, result in zip(group, group_results):
                        if not isinstance(result, Exception):
                            results[agent_name.lower()] = result

            # Implement fallback strategy if no results were obtained
            if not results and "PLANNER" in self.agents:
                planner_result = await self.agents["PLANNER"](state)
                results["planner"] = planner_result

            print("agent_outputs", results)

            # Return structured results
            return {
                "results": {
                    "agent_outputs": results
                }
            }

        except Exception as e:
            print(f"Execution error: {e}")
            # Emergency fallback with minimal response
            return {
                "results": {
                    "agent_outputs": {
                        "planner": {
                            "plan": "Emergency fallback plan: Please try again or contact support."
                        }
                    }
                }
            }
