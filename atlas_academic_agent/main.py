"""
Main entry point for ATLAS - Academic Task Learning Agent System.

This module provides the main interface for running the academic assistance system.
"""

import os
import sys
import json
import asyncio
import platform
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Windows-specific asyncio configuration
if platform.system() == 'Windows':
    # Set WindowsSelectorEventLoopPolicy for better compatibility
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables
load_dotenv()

from atlas.llm import NeMoLLaMa
from atlas.data_manager import DataManager
from atlas.workflow import create_agents_graph


# Set API key from environment
NEMOTRON_4_340B_INSTRUCT_KEY = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY")

# Import coordinator module and set LLM instance
import atlas.coordinator as coordinator_module


async def run_all_system(profile_json: str, calendar_json: str, task_json: str):
    """
    Run the entire academic assistance system with improved output handling.
    
    This is the main entry point for the ATLAS (Academic Task Learning Agent System).
    It handles initialization, user interaction, workflow execution, and result presentation.
    
    Args:
        profile_json: JSON string containing student profile data
        calendar_json: JSON string containing calendar/schedule data
        task_json: JSON string containing academic tasks data
        
    Returns:
        Tuple containing coordinator output and final state, or (None, None) on error
        
    Features:
        - Rich console interface with status updates
        - Async streaming of workflow steps
        - Comprehensive error handling
        - Live progress feedback
    """
    try:
        # Initialize rich console for enhanced UI
        console = Console()

        # Display welcome banner
        console.print("\n[bold magenta]🎓 ATLAS: Academic Task Learning Agent System[/bold magenta]")
        console.print("[italic blue]Initializing academic support system...[/italic blue]\n")

        # Initialize core system components
        llm = NeMoLLaMa(NEMOTRON_4_340B_INSTRUCT_KEY)
        
        # Set the global LLM instance for coordinator module
        coordinator_module.llm = llm

        # DataManager handles all data loading and access
        dm = DataManager()
        dm.load_data(profile_json, calendar_json, task_json)

        # Get user request
        console.print("[bold green]Please enter your academic request:[/bold green]")
        user_input = input()
        console.print(f"\n[dim italic]Processing request: {user_input}[/dim italic]\n")

        # Construct initial state object
        state = {
            "messages": [HumanMessage(content=user_input)],
            "profile": dm.get_student_profile("student_123"),
            "calendar": {"events": dm.get_upcoming_events()},
            "tasks": {"tasks": dm.get_active_tasks()},
            "results": {}
        }

        # Initialize workflow graph for agent orchestration
        graph = create_agents_graph(llm)

        console.print("[bold cyan]System initialized and processing request...[/bold cyan]\n")

        # Track important state transitions
        coordinator_output = None
        final_state = None

        # Process workflow with live status updates
        with console.status("[bold green]Processing...", spinner="dots") as status:
            # Stream workflow steps asynchronously
            async for step in graph.astream(state):
                # Capture coordinator analysis when available
                if "coordinator_analysis" in step.get("results", {}):
                    coordinator_output = step
                    analysis = coordinator_output["results"]["coordinator_analysis"]

                    # Display selected agents for transparency
                    console.print("\n[bold cyan]Selected Agents:[/bold cyan]")
                    for agent in analysis.get("required_agents", []):
                        console.print(f"• {agent}")

                # Capture final execution state
                if "execute" in step:
                    final_state = step

        # Display formatted results if available
        if final_state:
            agent_outputs = final_state.get("execute", {}).get("results", {}).get("agent_outputs", {})

            # Simple console output for each agent
            for agent, output in agent_outputs.items():
                console.print(f"\n[bold cyan]{agent.upper()} Output:[/bold cyan]")

                # Handle nested dictionary output
                if isinstance(output, dict):
                    for key, value in output.items():
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subvalue and isinstance(subvalue, str):
                                    console.print(subvalue.strip())
                        elif value and isinstance(value, str):
                            console.print(value.strip())
                # Handle direct string output
                elif isinstance(output, str):
                    console.print(output.strip())

        # Indicate completion
        console.print("\n[bold green]✓[/bold green] [bold]Task completed![/bold]")
        return coordinator_output, final_state

    except Exception as e:
        # Comprehensive error handling with stack trace
        console.print(f"\n[bold red]System error:[/bold red] {str(e)}")
        console.print("[yellow]Stack trace:[/yellow]")
        import traceback
        console.print(traceback.format_exc())
        return None, None


def load_sample_data():
    """
    Load sample data files for testing.
    
    Returns:
        Tuple of (profile_json, calendar_json, task_json) strings
    """
    # Get the directory where this script is located (Windows-compatible)
    current_dir = Path(__file__).parent.resolve()
    data_dir = current_dir / "data"
    
    # Try to load sample data files
    try:
        profile_path = data_dir / "profile.json"
        calendar_path = data_dir / "calendar.json"
        task_path = data_dir / "task.json"
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_json = f.read()
        with open(calendar_path, 'r', encoding='utf-8') as f:
            calendar_json = f.read()
        with open(task_path, 'r', encoding='utf-8') as f:
            task_json = f.read()
        return profile_json, calendar_json, task_json
    except FileNotFoundError as e:
        print(f"Error: Sample data files not found. Please create them in the data directory.")
        print(f"Missing file: {e.filename}")
        print(f"\nExpected location: {data_dir}")
        return None, None, None


async def main():
    """
    Main function to run the ATLAS system with sample data.
    """
    # Check if API key is configured
    if not NEMOTRON_4_340B_INSTRUCT_KEY:
        print("Error: NEMOTRON_4_340B_INSTRUCT_KEY not set in environment variables.")
        print("Please create a .env file with your API key.")
        return
    
    # Load sample data
    profile_json, calendar_json, task_json = load_sample_data()
    
    if not all([profile_json, calendar_json, task_json]):
        print("\nPlease provide the following JSON files in the data directory:")
        print("  - profile.json")
        print("  - calendar.json")
        print("  - task.json")
        print("\nSee .env.example and README.md for setup instructions.")
        return
    
    # Run the system
    await run_all_system(profile_json, calendar_json, task_json)


if __name__ == "__main__":
    asyncio.run(main())
