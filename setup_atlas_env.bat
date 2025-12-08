@echo off
REM 自动配置 atlas_academic_agent 项目的虚拟环境

echo 正在为 atlas_academic_agent 项目配置虚拟环境...

REM 检查是否存在虚拟环境
if not exist "atlas_academic_agent\venv" (
    echo 创建虚拟环境...
    python -m venv atlas_academic_agent\venv
)

echo 激活虚拟环境...
call atlas_academic_agent\venv\Scripts\activate.bat

echo 安装依赖...
pip install -r atlas_academic_agent\requirements.txt

echo.
echo ============================================
echo atlas_academic_agent 项目环境配置完成！
echo ============================================
echo.
echo 请在 IDE 中：
echo 1. 打开命令面板 (Ctrl+Shift+P)
echo 2. 选择 "Python: Select Interpreter"
echo 3. 选择 "atlas_academic_agent\venv\Scripts\python.exe"
echo ============================================
pause
