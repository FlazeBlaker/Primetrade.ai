# Binance Futures Order Bot

A CLI-based trading bot for Binance USDT-M Futures.

## Setup

1.  **Requirements**: Python 3.8+
2.  **Configuration**: Create a `config.py` file in `binance_bot/` or set environment variables:
    ```python
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    BASE_URL = "https://testnet.binancefuture.com" # Use 'https://fapi.binance.com' for real trading
    ```

## Usage

Run the bot from the `binance_bot` directory:

```bash
# Market Order
python src/main.py market --symbol BTCUSDT --side BUY --qty 0.001

# Limit Order
python src/main.py limit --symbol BTCUSDT --side SELL --qty 0.001 --price 50000

# Help
python src/main.py --help
```

## Logging

All actions are logged to `bot.log` with timestamps.
