# Hyperliquid Trading Bot

AI-powered async trading bot for Hyperliquid DEX using LangChain, asyncio, and RAG.

## 개요 (Overview)

비동기 처리, AI 에이전트, 블록체인 통합, RAG를 활용한 자동 트레이딩 봇:
- ✨ UI 깔끔하게 설계
- 📊 핵심 요소 모니터링
- 🔍 로직 검색 쉽게 구성

---

## Features

### 🤖 AI-Powered Trading
- **LangChain Agents**: Market analysis, sentiment analysis, and intelligent decision making
- **RAG Integration**: Historical pattern retrieval using vector databases
- **Explainable AI**: Transparent reasoning chains for all trading decisions

### ⚡ High-Performance Async
- **Non-blocking I/O**: Concurrent operations using asyncio
- **Real-time WebSocket**: Live market data streaming
- **Parallel Processing**: Multiple market monitoring and order execution

### 🛡️ Risk Management
- **Position Sizing**: Automated calculation based on risk parameters
- **Stop-Loss/Take-Profit**: Dynamic adjustment based on market conditions
- **Portfolio Monitoring**: Real-time exposure and risk tracking

### 📈 Extensible Strategy System
- **Plugin Architecture**: Easy strategy development and integration
- **Backtesting Framework**: Historical performance validation
- **Multiple Strategies**: Trend following, mean reversion, breakout, and AI-driven

### 📊 Monitoring & Observability
- **Rich Dashboard**: Terminal-based real-time monitoring
- **Comprehensive Logging**: Structured logging with Loguru
- **Performance Metrics**: Track KPIs, win rate, Sharpe ratio, and more

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│  (CLI/Dashboard - Real-time monitoring & control)               │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                     Application Core Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Bot        │  │  Strategy    │  │   Risk Manager      │  │
│  │  Orchestrator│◄─┤   Engine     │◄─┤   (Position/Loss)   │  │
│  └──────┬───────┘  └──────────────┘  └─────────────────────┘  │
└─────────┼──────────────────────────────────────────────────────┘
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                  LangChain AI Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Market     │  │  Sentiment   │  │   Decision Agent    │  │
│  │  Analyzer    │  │  Analyzer    │  │  (ReAct/Function)   │  │
│  │   Agent      │  │   Agent      │  │                     │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │
┌─────────▼──────────────────────────────────────────────────────┐
│              Async Service Layer (asyncio)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Hyperliquid │  │   Market     │  │   Event Processor   │  │
│  │   Client     │  │   Data       │  │   (WebSocket)       │  │
│  │   (REST/WS)  │  │   Service    │  │                     │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                   Data & Storage Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │   Vector DB  │  │   Time-Series│  │   State Manager     │  │
│  │  (Chroma/    │  │   DB (Redis/ │  │   (Positions/       │  │
│  │   Pinecone)  │  │   InfluxDB)  │  │    Orders)          │  │
│  └──────────────┘  └──────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Git
- API Keys: OpenAI, LangSmith (optional), Hyperliquid wallet

### Installation

```bash
# Clone repository
git clone https://github.com/nubro999/async_rag_py.git
cd pythonST

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env and add your credentials:
# - WALLET_ADDRESS
# - PRIVATE_KEY
# - OPENAI_API_KEY
# - LANGCHAIN_API_KEY (optional)
# - Database URLs (if using external services)
```

### Initialize Databases

```bash
python scripts/setup_db.py
```

### Run the Bot

```bash
# Development mode
python main.py
```

See [QUICKSTART.md](QUICKSTART.md) and [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed instructions.

---

## Project Structure

```
pythonST/
├── src/                    # Source code
│   ├── core/              # Bot orchestrator, strategy engine, risk manager
│   ├── agents/            # LangChain AI agents
│   ├── services/          # Hyperliquid client, market data, events
│   ├── storage/           # Vector DB, time-series DB, state manager
│   ├── models/            # Data models (Order, Position, Market Data)
│   ├── strategies/        # Trading strategies
│   ├── indicators/        # Technical indicators
│   └── ui/                # User interface components
├── config/                # Configuration files
│   ├── config.yaml        # Main configuration
│   ├── strategies.yaml    # Strategy parameters
│   └── logging.yaml       # Logging configuration
├── data/                  # Data storage
│   ├── vectors/          # Vector database
│   ├── cache/            # Cache files
│   └── logs/             # Log files
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── tests/                 # Test files
├── async/                 # Async examples
├── main.py               # Application entry point
├── pyproject.toml        # Project configuration
└── requirements.txt      # Dependencies
```

---

## Technology Stack

### Core
- **Python 3.11+**: Main language
- **asyncio**: Asynchronous I/O
- **aiohttp**: Async HTTP client
- **websockets**: WebSocket client

### LangChain Stack
- **LangChain**: AI agent framework
- **LangGraph**: Agent workflow orchestration
- **OpenAI/Anthropic**: LLM providers
- **LangSmith**: Monitoring and debugging

### Hyperliquid Integration
- **Hyperliquid SDK**: DEX API integration
- **eth-account**: Wallet management
- **web3**: Blockchain interactions

### Data & Storage
- **ChromaDB/Pinecone**: Vector database for RAG
- **Redis**: State management and caching
- **InfluxDB/TimescaleDB**: Time-series data
- **Pydantic**: Data validation

### Monitoring
- **Loguru**: Advanced logging
- **Rich**: Terminal UI
- **Prometheus**: Metrics collection (optional)

---

## Configuration

### Trading Parameters

Edit `config/config.yaml`:

```yaml
trading:
  max_position_size: 0.1      # 10% of portfolio per position
  max_positions: 5            # Maximum concurrent positions
  default_leverage: 2         # Default leverage
  risk_per_trade: 0.02        # 2% risk per trade

risk:
  use_stop_loss: true
  default_stop_loss_percent: 2.0    # 2% stop loss
  default_take_profit_percent: 5.0  # 5% take profit
  max_daily_loss: 5.0              # 5% max daily loss
```

### Strategies

Edit `config/strategies.yaml`:

```yaml
strategies:
  trend_following:
    enabled: true
    params:
      timeframe: "1h"
      ema_short: 12
      ema_long: 26
      rsi_period: 14

  ai_decision:
    enabled: true
    params:
      model: "gpt-4-turbo"
      confidence_threshold: 0.7
```

---

## Development

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black src/

# Linting
ruff check src/

# Type checking
mypy src/
```

### Project Setup

```bash
# Install development dependencies
pip install -e ".[dev]"
```

---

## Implementation Status

### ✅ Completed
- [x] Project structure and architecture
- [x] Core module scaffolding
- [x] Data models (Pydantic)
- [x] Configuration system
- [x] Logging setup

### 🚧 In Progress
- [ ] Hyperliquid API integration
- [ ] LangChain agent implementation
- [ ] WebSocket event handling
- [ ] Database connections

### 📋 Planned
- [ ] Strategy implementations
- [ ] Technical indicators
- [ ] Backtesting framework
- [ ] Dashboard UI
- [ ] Performance monitoring
- [ ] Alerting system

---

## Safety & Risk Management

### ⚠️ Important Warnings

- **Never commit** private keys or API credentials
- **Start with testnet** before using real funds
- **Set strict limits** on position sizes and leverage
- **Monitor actively** when bot is running
- **Use stop-losses** on all positions
- **Test thoroughly** before live trading

### Risk Controls

- Position size limits
- Maximum concurrent positions
- Daily loss limits
- Maximum drawdown thresholds
- Leverage restrictions
- Stop-loss enforcement

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

MIT License - see LICENSE file for details

---

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed system architecture
- [QUICKSTART.md](QUICKSTART.md) - Quick reference guide
- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) - Installation guide
- [async/async.py](async/async.py) - Async programming examples

---

## Support

- **Issues**: [GitHub Issues](https://github.com/nubro999/async_rag_py/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nubro999/async_rag_py/discussions)
- **Email**: zcb167@gmail.com

---

## Acknowledgments

Built with:
- LangChain for AI capabilities
- Hyperliquid for DEX integration
- Python asyncio for high performance
- Open source community

---
