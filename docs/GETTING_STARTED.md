# Getting Started with Hyperliquid Trading Bot

## Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nubro999/async_rag_py.git
cd pythonST
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

Edit `.env` and add your credentials:

```env
# Hyperliquid Configuration
WALLET_ADDRESS=your_wallet_address
PRIVATE_KEY=your_private_key

# LangChain/OpenAI
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key

# Database URLs (if using external databases)
REDIS_URL=redis://localhost:6379
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your_influxdb_token
```

### 5. Initialize Databases

```bash
python scripts/setup_db.py
```

## Running the Bot

### Development Mode

```bash
python main.py
```

### With Custom Configuration

```bash
# Edit config/config.yaml first, then:
python main.py
```

## Project Structure

```
pythonST/
├── src/              # Source code
│   ├── core/         # Core bot components
│   ├── agents/       # LangChain AI agents
│   ├── services/     # External service integrations
│   ├── storage/      # Database wrappers
│   ├── models/       # Data models
│   └── strategies/   # Trading strategies
├── config/           # Configuration files
├── tests/            # Test files
├── scripts/          # Utility scripts
├── data/             # Data storage
└── docs/             # Documentation
```

## Next Steps

1. Read [ARCHITECTURE.md](../ARCHITECTURE.md) for system design
2. Configure your trading strategies in `config/strategies.yaml`
3. Review risk management settings in `config/config.yaml`
4. Set up monitoring and logging
5. Test in paper trading mode first

## Safety Warnings

⚠️ **Important:**
- Never commit your `.env` file or private keys
- Start with testnet before using real funds
- Set appropriate risk limits
- Monitor the bot regularly
- Use stop-losses and position limits

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Make sure you're in the virtual environment
pip install -r requirements.txt
```

**Configuration errors:**
```bash
# Check your .env file has all required variables
# Verify config/config.yaml is valid YAML
```

**Connection errors:**
```bash
# Check your API keys are correct
# Verify network connectivity
# Check database services are running
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/nubro999/async_rag_py/issues
- Documentation: See `docs/` directory

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
ruff check src/
```

### Type Checking

```bash
mypy src/
```
