# ATLAS - Academic Task Learning Agent System

A sophisticated multi-agent system built with LangGraph for academic assistance, featuring specialized agents for planning, note-taking, and academic advising. **Cross-platform support for Windows, Linux, and macOS.**

---

## 馃搵 Table of Contents

- [Overview](#-overview)
- [Features](#-key-features)
- [Quick Start](#-quick-start)
  - [Windows Setup](#windows-setup)
  - [Linux/Mac Setup](#linuxmac-setup)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Virtual Environment Setup](#virtual-environment-setup-recommended)
  - [Manual Setup](#manual-setup-advanced)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Configuration](#锔?configuration)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [License](#-license)

---

## 馃帗 Overview

ATLAS is an AI-powered academic support system that helps students manage their studies through intelligent agent coordination. It uses the ReACT (Reasoning and Acting) framework to provide personalized assistance based on individual learning styles, schedules, and academic needs.

### Key Features

- **Multi-Agent Architecture**: Three specialized agents working in coordination
  - **PlannerAgent**: Scheduling, time management, and study plan generation
  - **NoteWriterAgent**: Personalized study material creation
  - **AdvisorAgent**: Academic guidance and support
  
- **Intelligent Coordination**: Dynamic agent selection based on student needs
- **Learning Style Adaptation**: Customized support based on individual preferences
- **ADHD-Friendly**: Special considerations for students with attention challenges
- **Parallel Execution**: Efficient concurrent agent processing
- **Cross-Platform**: Works on Windows, Linux, and macOS

---

## 馃殌 Quick Start

### Windows Setup

**Option 1: One-Click Setup (Easiest!)**

1. Double-click `setup_venv.bat` (creates virtual environment & installs dependencies)
2. Double-click `run.bat` (starts ATLAS)

That's it! No command line needed.

**Option 2: Command Line**

```cmd
:: First time setup
setup_venv.bat

:: Run ATLAS
run.bat
```

**Option 3: PowerShell**

```powershell
# First time setup
.\setup_venv.ps1

# Run ATLAS
.\run.ps1
```

*Note: If you get execution policy errors:*
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

### Linux/Mac Setup

**Option 1: Terminal Setup**

```bash
# Make scripts executable (first time only)
chmod +x setup.sh run.sh

# First time setup
./setup.sh

# Run ATLAS
./run.sh
```

**Option 2: Manual Commands**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your API key

# Run the application
python main.py
```

---

## 馃摝 Installation

### Prerequisites

- **Python 3.9+** (Windows, Linux, or macOS)
- **NVIDIA NeMo API key** (for LLM access)
- **Git** (optional, for cloning repository)

### Virtual Environment Setup (Recommended)

Virtual environments keep dependencies isolated from your system Python, preventing conflicts and keeping your system clean.

#### Why Use Virtual Environments?

鉁?Keeps dependencies isolated from system Python  
鉁?Avoids version conflicts with other projects  
鉁?Makes it easy to share your setup  
鉁?Ensures reproducible installations  
鉁?Keeps your system clean  

#### Setup Instructions

**Windows:**
```cmd
setup_venv.bat    # Creates venv and installs dependencies
run.bat           # Runs ATLAS (auto-activates venv)
```

**Linux/Mac:**
```bash
./setup.sh        # Creates venv and installs dependencies
./run.sh          # Runs ATLAS (auto-activates venv)
```

The setup scripts will:
1. Check Python installation
2. Create virtual environment in `venv/` folder
3. Activate the environment
4. Upgrade pip
5. Install all dependencies from `requirements.txt`
6. Verify installation

This takes 2-5 minutes depending on your internet speed.

### Manual Setup (Advanced)

If you prefer not to use virtual environments (not recommended):

**Windows:**
```cmd
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API key
python main.py
```

**Linux/Mac:**
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
python main.py
```

鈿狅笍 **Warning**: Installing globally may cause conflicts with other projects!

---

## 馃幆 Usage

### Running ATLAS

After setup, simply run the appropriate script for your platform:

**Windows:**
```cmd
run.bat              # Command Prompt
# or
.\run.ps1            # PowerShell
```

**Linux/Mac:**
```bash
./run.sh
```

The scripts will automatically:
- 鉁?Check/create virtual environment
- 鉁?Activate the environment
- 鉁?Verify dependencies
- 鉁?Launch ATLAS

### Entering Requests

When prompted, enter your academic request, such as:

- "Help me prepare for my Advanced Algorithms exam next week"
- "Create study notes for Machine Learning concepts"
- "I need help managing multiple deadlines this month"
- "Plan my study schedule considering my ADHD and football practice"

### Sample Data

The system comes with sample data for testing:
- **Student Profile**: Alex Johnson, CS Junior with ADHD
- **Calendar**: Lectures, labs, football practice
- **Tasks**: Assignments due in May 2026

You can customize these files in the `data/` directory.

---

## 馃搧 Project Structure

```
atlas_academic_agent/
鈹溾攢鈹€ atlas/                      # Main Python package
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ state.py               # State definitions & data models
鈹?  鈹溾攢鈹€ llm.py                 # LLM client (NVIDIA NeMo)
鈹?  鈹溾攢鈹€ data_manager.py        # Data management system
鈹?  鈹溾攢鈹€ coordinator.py         # Coordinator agent
鈹?  鈹溾攢鈹€ executor.py            # Agent execution orchestrator
鈹?  鈹溾攢鈹€ workflow.py            # LangGraph workflow orchestration
鈹?  鈹斺攢鈹€ agents/                # Specialized agent modules
鈹?      鈹溾攢鈹€ __init__.py
鈹?      鈹溾攢鈹€ base_agent.py      # ReActAgent base class
鈹?      鈹溾攢鈹€ planner_agent.py   # Planning & scheduling
鈹?      鈹溾攢鈹€ notewriter_agent.py # Study material generation
鈹?      鈹斺攢鈹€ advisor_agent.py   # Academic guidance
鈹溾攢鈹€ data/                       # Sample data files
鈹?  鈹溾攢鈹€ profile.json           # Student profile
鈹?  鈹溾攢鈹€ calendar.json          # Calendar events
鈹?  鈹斺攢鈹€ task.json              # Academic tasks
鈹溾攢鈹€ venv/                       # Virtual environment (created by setup)
鈹溾攢鈹€ main.py                     # Application entry point
鈹溾攢鈹€ requirements.txt            # Python dependencies
鈹溾攢鈹€ .env.example               # Environment variable template
鈹溾攢鈹€ setup_venv.bat             # Windows setup script
鈹溾攢鈹€ setup_venv.ps1             # Windows PowerShell setup
鈹溾攢鈹€ setup.sh                   # Linux/Mac setup script
鈹溾攢鈹€ run.bat                    # Windows run script
鈹溾攢鈹€ run.ps1                    # Windows PowerShell run
鈹溾攢鈹€ run.sh                     # Linux/Mac run script
鈹斺攢鈹€ README.md                  # This file
```

**Note**: The `venv/` directory is ~500MB-1GB and should NOT be committed to Git (it's in `.gitignore`).

---

## 馃彈锔?Architecture

### ReACT Framework

ATLAS uses the ReACT (Reasoning and Acting) pattern:
1. **Thought**: Analyze the situation and determine needs
2. **Action**: Select appropriate tools or agents
3. **Observation**: Evaluate results and insights
4. **Decision**: Formulate final response or plan

### Agent Coordination Flow

```
User Request 鈫?Coordinator 鈫?Profile Analyzer 鈫?Parallel Agents 鈫?Executor 鈫?Results
                     鈫?              Determines which agents needed:
              - Planner (scheduling)
              - NoteWriter (study materials)
              - Advisor (guidance)
```

### Workflow Graph

The system uses LangGraph's StateGraph for orchestration:
- Conditional routing based on request analysis
- Parallel execution of compatible agents
- State management across agent interactions
- Fallback mechanisms for robustness

---

## 鈿欙笍 Configuration

### API Key Setup

1. Copy the example environment file:
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. Edit `.env` and add your NVIDIA NeMo API key:
   ```
   NEMOTRON_4_340B_INSTRUCT_KEY=your_api_key_here
   ```

3. Get your API key from [NVIDIA NeMo](https://developer.nvidia.com/nemo)

### Customizing Data

Modify JSON files in the `data/` directory:

- **profile.json**: Student information, learning preferences, courses
- **calendar.json**: Upcoming events and schedule
- **task.json**: Assignments, projects, and deadlines

### LLM Settings

Modify `atlas/llm.py` to adjust:
- Model selection
- Temperature (creativity level)
- Max tokens
- Base URL (for different providers)

---

## 馃敡 Troubleshooting

### Common Issues

#### Windows

**Problem**: `'python' is not recognized`
- **Solution**: Add Python to PATH during installation, or reinstall Python with "Add to PATH" checked

**Problem**: PowerShell execution policy error
- **Solution**: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**Problem**: Virtual environment not activating
- **Solution**: Delete `venv/` folder and run `setup_venv.bat` again

#### Linux/Mac

**Problem**: `python3: command not found`
- **Solution**: Install Python 3.9+: `sudo apt-get install python3.9` (Ubuntu) or `brew install python3` (Mac)

**Problem**: Permission denied on scripts
- **Solution**: Run `chmod +x setup.sh run.sh`

**Problem**: `python3-venv` not found
- **Solution**: Install it: `sudo apt-get install python3-venv` (Ubuntu/Debian)

#### All Platforms

**Problem**: Dependencies fail to install
- **Solution**: 
  ```bash
  # Activate venv first
  # Windows: venv\Scripts\activate.bat
  # Linux/Mac: source venv/bin/activate
  
  # Upgrade pip
  pip install --upgrade pip
  
  # Try installing again
  pip install -r requirements.txt
  ```

**Problem**: API key errors
- **Solution**: Ensure `.env` file exists and contains valid API key

**Problem**: Missing data files
- **Solution**: Check that JSON files exist in `data/` directory

### Getting Help

1. Check error messages carefully
2. Verify Python version: `python --version` (should be 3.9+)
3. Ensure virtual environment is activated
4. Check `.env` file configuration
5. Review sample data format

For more detailed troubleshooting, see platform-specific guides online.

---

## 馃捇 Development

### Adding New Agents

1. Create new agent class inheriting from `ReActAgent`
2. Implement workflow using `StateGraph`
3. Register agent in `AgentExecutor`
4. Update coordinator prompt

### Modifying Prompts

Agent prompts are defined as constants in each agent module. Customize:
- Analysis frameworks
- Output formats
- Few-shot examples
- Response structures

### Code Structure

- **state.py**: Defines `AcademicState` TypedDict and data models
- **llm.py**: NeMoLLaMa class for LLM interaction
- **agents/**: Specialized agent implementations
- **workflow.py**: LangGraph orchestration
- **coordinator.py**: Agent selection logic

---

## 馃摑 Example Requests

Try these to test different agent combinations:

1. **Planning-focused**: 
   > "I have an exam tomorrow and football practice tonight. Help me study efficiently."

2. **Note-taking focused**: 
   > "Create quick review notes for Calculus III focusing on vector calculus."

3. **Advisory focused**: 
   > "I'm struggling with time management and have multiple deadlines. What should I do?"

4. **Combined**: 
   > "Help me balance studying for Advanced Algorithms while managing my ML project deadline."

---

## 馃實 Cross-Platform Compatibility

ATLAS is designed to work seamlessly across platforms:

| Feature | Windows | Linux | macOS |
|---------|---------|-------|-------|
| Virtual Environment | 鉁?| 鉁?| 鉁?|
| Async/Await | 鉁?| 鉁?| 鉁?|
| Path Handling | 鉁?| 鉁?| 鉁?|
| Rich Console UI | 鉁?| 鉁?| 鉁?|
| Auto-setup Scripts | 鉁?| 鉁?| 鉁?|

### Platform-Specific Notes

**Windows:**
- Uses `WindowsSelectorEventLoopPolicy` for asyncio
- Batch (.bat) and PowerShell (.ps1) scripts provided
- Path separators handled automatically via `pathlib.Path`

**Linux/Mac:**
- Standard Unix shell scripts (.sh)
- Uses `python3` command
- Bash-compatible scripts

---

## 馃搫 License

This project is part of the GenAI_Agents repository. Refer to the main repository license for usage terms.

---

## 馃 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 馃檹 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses [NVIDIA NeMo](https://developer.nvidia.com/nemo) for LLM capabilities
- Inspired by ReACT framework for agent reasoning
- Rich library for beautiful terminal output

---

## 馃摓 Support

- **Documentation**: This README covers most common scenarios
- **Issues**: Report bugs with platform, Python version, and error details
- **Questions**: Include your OS, Python version, and steps to reproduce

---

**Happy Studying! 馃帗鉁?*

*Built with 鉂わ笍 for students everywhere*
