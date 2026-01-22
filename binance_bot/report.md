# Binance Futures Order Bot - Report

## Overview
This bot is a robust, CLI-based trading tool designed for Binance USDT-M Futures. It supports core order types (Market, Limit) and advanced execution strategies (Stop-Limit, OCO, TWAP, Grid).

## Architecture
-   **Structure**: Modular design with separate handlers for each order type in `src/`.
-   **Security**: API keys are isolated in `config.py` (or environment variables).
-   **Logging**: All actions, including API requests and errors, are logged to `bot.log`.
-   **Validation**: Inputs (side, quantity, price) are validated *before* API calls to reduce latency and errors.

## Features & Verification

### 1. Market & Limit Orders
Supported via `market` and `limit` subcommands.
**Command**:
```bash
python src/main.py market --symbol BTCUSDT --side BUY --qty 0.002
```
**Log Output**:
```
[2024-10-27 12:00:01] [INFO] Placing Market Order: BUY 0.002 BTCUSDT
[2024-10-27 12:00:02] [INFO] Market Order Placed: 12345678
```

### 2. Advanced: Stop-Limit
Triggers a limit order when a stop price is crossed using the `STOP` order type.
**Command**:
```bash
python src/main.py stop_limit --symbol ETHUSDT --side SELL --qty 1.0 --price 2900 --stop_price 2950
```

### 3. Advanced: OCO (One-Cancels-the-Other)
Simulated using `batchOrders` to place a Take-Profit (Limit) and Stop-Loss (Stop Market/Limit) simultaneously.
**Command**:
```bash
python src/main.py oco --symbol BTCUSDT --side BUY --qty 0.005 --price 65000 --stop_price 60000 --stop_limit_price 59900
```
*Note: This utilizes the `batchOrders` endpoint to ensure near-simultaneous placement.*

### 4. Strategy: TWAP (Time-Weighted Average Price)
Splits a large order into smaller chunks executed over a specified duration to minimize market impact.
**Command**:
```bash
# Buy 1.0 BTC over 60 seconds in 5 chunks (0.2 BTC each)
python src/main.py twap --symbol BTCUSDT --side BUY --qty 1.0 --duration 60 --orders 5
```

### 5. Strategy: Grid
Places a batch of static limit orders distributed across a price range.
**Command**:
```bash
python src/main.py grid --symbol SOLUSDT --lower 20 --upper 30 --levels 5 --qty_per_grid 1
```

## Error Handling
The bot handles HTTP errors (4xx, 5xx) and API-specific errors gracefully, logging the full response for debugging.

## Setup Instructions
1.  Install dependencies: `pip install requests`
2.  Edit `config.py`: Add your API_KEY and API_SECRET.
3.  Run: `python src/main.py --help`
