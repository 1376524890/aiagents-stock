@echo off

REM Windows环境配置脚本
REM 用于配置AI股票分析系统的运行环境

color 0A

echo =====================================
echo AI股票分析系统环境配置脚本
echo =====================================
echo.

REM 1. 检查Python 3是否安装
echo 1. 检查Python 3是否安装...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✓ Python 3已安装: %PYTHON_VERSION%
) else (
    echo ✗ Python 3未安装，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 2. 检查pip是否安装
echo 2. 检查pip是否安装...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
    echo ✓ pip已安装: %PIP_VERSION%
) else (
    echo 正在安装pip...
    python -m ensurepip --upgrade
    echo ✓ pip安装成功
)

REM 3. 检查虚拟环境是否存在，不存在则创建
echo 3. 检查虚拟环境是否存在...
set VENV_DIR=venv
if exist "%VENV_DIR%" (
    echo ✓ 虚拟环境已存在: %VENV_DIR%
) else (
    echo 虚拟环境不存在，正在创建...
    python -m venv "%VENV_DIR%"
    echo ✓ 虚拟环境创建成功: %VENV_DIR%
)

REM 4. 激活虚拟环境
echo 4. 激活虚拟环境...
call "%VENV_DIR%\Scripts\activate"

REM 5. 升级pip
echo 5. 升级pip...
pip install --upgrade pip >nul 2>&1
echo ✓ pip升级完成

REM 6. 安装Python依赖
echo 6. 安装Python依赖...
if exist "requirements.txt" (
    REM 使用pip安装依赖，已安装则跳过
    pip install -r requirements.txt
    echo ✓ Python依赖安装完成
) else (
    echo ✗ requirements.txt文件未找到
    pause
    exit /b 1
)

REM 7. 显示环境设置完成信息
echo.
echo =====================================
echo 环境配置完成！
echo =====================================
echo.
echo 使用说明：
echo 1. 激活虚拟环境: %VENV_DIR%\Scripts\activate
REM echo 2. 运行应用: streamlit run app.py
echo 2. 运行应用: python run.py
echo.
echo 按任意键退出...
pause >nul
