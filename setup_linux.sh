#!/bin/bash

# Linux环境配置脚本
# 用于配置AI股票分析系统的运行环境

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}AI股票分析系统环境配置脚本${NC}"
echo -e "${GREEN}=====================================${NC}"

# 1. 检查Python 3是否安装
echo -e "${YELLOW}1. 检查Python 3是否安装...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python 3已安装: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3未安装，请先安装Python 3.8或更高版本${NC}"
    exit 1
fi

# 2. 检查pip是否安装
echo -e "${YELLOW}2. 检查pip是否安装...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ pip已安装: $PIP_VERSION${NC}"
else
    echo -e "${YELLOW}pip未安装，尝试安装...${NC}"
    python3 -m ensurepip --upgrade
    echo -e "${GREEN}✓ pip安装成功${NC}"
fi

# 3. 检查虚拟环境是否存在，不存在则创建
echo -e "${YELLOW}3. 检查虚拟环境是否存在...${NC}"
VENV_DIR="venv"
if [ -d "$VENV_DIR" ]; then
    echo -e "${GREEN}✓ 虚拟环境已存在: $VENV_DIR${NC}"
else
    echo -e "${YELLOW}虚拟环境不存在，正在创建...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ 虚拟环境创建成功: $VENV_DIR${NC}"
fi

# 4. 激活虚拟环境
echo -e "${YELLOW}4. 激活虚拟环境...${NC}"
source "$VENV_DIR/bin/activate"

# 5. 升级pip
echo -e "${YELLOW}5. 升级pip...${NC}"
pip install --upgrade pip

# 6. 检查并安装chromium-browser
echo -e "${YELLOW}6. 检查chromium-browser是否安装...${NC}"
if command -v chromium-browser &> /dev/null; then
    echo -e "${GREEN}✓ chromium-browser已安装${NC}"
else
    echo -e "${YELLOW}chromium-browser未安装，正在安装...${NC}"
    sudo apt-get update
    sudo apt-get install -y chromium-browser
    echo -e "${GREEN}✓ chromium-browser安装成功${NC}"
fi

# 7. 安装Python依赖
echo -e "${YELLOW}7. 安装Python依赖...${NC}"
if [ -f "requirements.txt" ]; then
    # 使用pip安装依赖，已安装则跳过
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Python依赖安装完成${NC}"
else
    echo -e "${RED}✗ requirements.txt文件未找到${NC}"
    exit 1
fi

# 8. 显示环境设置完成信息
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}环境配置完成！${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "${YELLOW}使用说明：${NC}"
echo -e "1. 激活虚拟环境: source $VENV_DIR/bin/activate"
echo -e "2. 运行应用: streamlit run app.py"
echo -e "3. 或运行: python run.py"
echo -e "${GREEN}=====================================${NC}"
