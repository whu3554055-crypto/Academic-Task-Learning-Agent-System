# Academic-Task-Learning-Agent-System

**Academic Task Learning Agent System（ATLAS）** 是基于 LangGraph 的多智能体学术辅助系统，帮助学生规划学习、整理笔记、获取个性化学业建议。

## 项目简介

本项目将规划、笔记、顾问三类专用智能体与协调器结合，根据学生档案、日程与任务自动分析需求，并行调度合适的智能体完成学业支持。系统支持 ADHD 友好型学习模式，适配不同学习风格，可在 Windows、Linux 与 macOS 上运行。

## 核心功能

- **PlannerAgent**：日程安排、时间管理与学习计划
- **NoteWriterAgent**：个性化学习材料与内容摘要
- **AdvisorAgent**：学业指导与问题解答
- **智能协调**：ReACT 框架驱动，按需并行执行多个智能体

## 技术栈

- LangGraph 工作流编排
- NVIDIA NeMo 大语言模型
- Python async/await 异步处理
- Rich 终端交互界面

## 项目结构

```
atlas_academic_agent/
├── atlas/                    # 核心 Python 包
│   ├── agents/              # 规划、笔记、顾问智能体
│   ├── coordinator.py       # 多智能体协调器
│   ├── workflow.py          # LangGraph 工作流
│   ├── executor.py          # 并行执行器
│   ├── state.py             # 状态定义
│   ├── llm.py               # LLM 客户端
│   └── data_manager.py      # 数据管理
├── data/                    # 示例数据
└── main.py                  # 应用入口
```

## 快速开始

详细安装与使用说明见 [atlas_academic_agent/README.md](atlas_academic_agent/README.md)。

```bash
cd atlas_academic_agent
# Windows: setup_venv.bat 后 run.bat
# Linux/Mac: ./setup.sh 后 ./run.sh
```

## 使用示例

- 「帮我准备下周的高级算法考试」
- 「为机器学习概念创建学习笔记」
- 「考虑到我的 ADHD 和足球训练，规划本月的学习时间表」
