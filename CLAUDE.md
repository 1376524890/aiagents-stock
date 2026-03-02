# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

天心多AI智能体股票分析系统 (Tianxin Multi-AI Agent Stock Analysis System) - A multi-AI agent stock analysis system for Chinese A-shares, Hong Kong stocks, and US stocks. The system simulates a securities analyst team with specialized AI agents working collaboratively.

## Common Commands

### Running the Application
```bash
# Using run.py (checks dependencies and config)
python run.py

# Direct Streamlit command
streamlit run app.py --server.port 8503 --server.address 0.0.0.0

# With virtual environment
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\Activate.ps1  # Windows PowerShell
streamlit run app.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Docker Deployment
```bash
# Using docker-compose
docker-compose up -d

# Manual build and run
docker build -t agentsstock1 .
docker run -d -p 8503:8501 -v $(pwd)/.env:/app/.env --name agentsstock1 agentsstock1
```

## Architecture

### Core Data Flow
```
User Input → StockDataFetcher → Data Processing → Multi-Agent Analysis → Team Discussion → Final Decision → PDF Report
```

### Key Modules

**Data Layer:**
- `stock_data.py` - Stock data fetching (yfinance, AKShare), technical indicator calculation
- `data_source_manager.py` - Multi-source data management with fallback (TDX → Tushare → AKShare)
- `fund_flow_akshare.py` - Fund flow data from AKShare
- `quarterly_report_data.py` - Quarterly financial reports via pywencai
- `risk_data_fetcher.py` - Risk data (share unlocks, insider selling) via pywencai

**AI Agent Layer:**
- `deepseek_client.py` - OpenAI-compatible API client for DeepSeek/other LLMs
- `ai_agents.py` - Core multi-agent system (Technical, Fundamental, Fund Flow, Risk, Market Sentiment, News analysts)
- `longhubang_agents.py` - Longhubang (龙虎榜) specialized agents
- `sector_strategy_agents.py` - Sector strategy agents (Macro, Sector Diagnosis, Fund Flow, Market Sentiment)
- `main_force_analysis.py` - Main force capital flow analysis

**Engine Layer:**
- `longhubang_engine.py` - Longhubang analysis orchestration
- `sector_strategy_engine.py` - Sector strategy analysis orchestration
- `smart_monitor_engine.py` - Smart monitoring engine for automated trading decisions

**UI Layer (Streamlit):**
- `app.py` - Main application entry point with sidebar navigation
- `longhubang_ui.py`, `sector_strategy_ui.py`, `main_force_ui.py`, `monitor_ui.py`, `smart_monitor_ui.py`, `portfolio_ui.py` - Feature-specific UI modules

**Services:**
- `monitor_service.py` - Background monitoring service
- `notification_service.py` - Email and Webhook (DingTalk/Feishu) notifications
- `portfolio_scheduler.py`, `sector_strategy_scheduler.py`, `monitor_scheduler.py` - Scheduled task management
- `miniqmt_interface.py` - MiniQMT trading interface for automated execution

**Database (SQLite + Peewee ORM):**
- `database.py`, `monitor_db.py`, `longhubang_db.py`, `portfolio_db.py`, `smart_monitor_db.py`, `sector_strategy_db.py`, `main_force_batch_db.py`

### Multi-Agent Analysis Pattern

The system uses parallel analysis with specialized agents:

```python
# From ai_agents.py - agents run in parallel, then results are synthesized
agents_results = {
    "technical": self.technical_analyst_agent(...),
    "fundamental": self.fundamental_analyst_agent(...),
    "fund_flow": self.fund_flow_analyst_agent(...),
    "risk_management": self.risk_management_agent(...),
    # ... more agents
}
# Team discussion synthesizes all agent outputs
discussion = self.conduct_team_discussion(agents_results, stock_info)
# Final decision generated
decision = self.final_decision(discussion, stock_info, indicators)
```

## Configuration

### Environment Variables (.env)
Required:
- `DEEPSEEK_API_KEY` - DeepSeek API key for LLM calls
- `DEEPSEEK_BASE_URL` - API endpoint (default: https://api.deepseek.com/v1)

Optional:
- `TUSHARE_TOKEN` - Tushare data source token
- `TDX_ENABLED`, `TDX_BASE_URL` - Local TDX data source
- `MINIQMT_*` - MiniQMT trading interface config
- `EMAIL_*` - Email notification settings
- `WEBHOOK_*` - DingTalk/Feishu webhook settings
- `TIMEZONE` - Default: Asia/Shanghai

### Model Selection
Models are defined in `model_config.py`. Supports DeepSeek, Qwen (阿里百炼), and SiliconFlow models. The system uses OpenAI-compatible API interface.

## Key Patterns

### Adding a New Analysis Feature
1. Create data fetcher module if needed (follow pattern in `stock_data.py`)
2. Create agent functions in dedicated `*_agents.py` file
3. Create engine module for orchestration (`*_engine.py`)
4. Create UI module (`*_ui.py`) with `display_*` function
5. Import and call UI function in `app.py` sidebar navigation
6. Create database module (`*_db.py`) if persistence needed
7. Create PDF generator (`*_pdf.py`) if report export needed

### Database Pattern
All database modules use Peewee ORM with SQLite. Tables are defined as Peewee Model classes. Use `database.py` as reference.

### UI Pattern
UI modules use Streamlit components. Main `app.py` handles navigation via sidebar radio buttons. Each feature module has a `display_*` function called from main app.

### API Client Pattern
`DeepSeekClient` wraps OpenAI SDK. All LLM calls go through `call_api()` method. For reasoner models, automatically extracts `reasoning_content` if present.

## Stock Code Formats
- A股: 6-digit code (000001, 600036)
- 港股: 1-5 digit code (700, 9988) or with HK prefix
- 美股: Letter code (AAPL, TSLA)

## Important Files
- `run.py` - Entry point with dependency checking
- `config.py` - Environment variable loading and configuration constants
- `config_manager.py` - Web UI for configuration management
- `model_config.py` - Available LLM model options

## Notes
- Default server port: 8503 (changed from 8501 to avoid conflicts)
- System designed for Chinese A-share T+1 trading rules
- PDF generation uses pyppeteer (Chrome headless) for Markdown-to-PDF conversion