import argparse
import sys
import os

# Ensure src is in pythonpath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.stop_limit import place_stop_limit_order
from src.advanced.oco import place_oco_order
from src.advanced.twap import execute_twap
from src.advanced.grid_strategy import execute_grid_strategy
from src.utils import logger

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    subparsers = parser.add_subparsers(dest="command", help="Order Type / Strategy")

    # Market Order
    market_parser = subparsers.add_parser("market", help="Place Market Order")
    market_parser.add_argument("--symbol", required=True, help="Trading Pair (e.g., BTCUSDT)")
    market_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order Side")
    market_parser.add_argument("--qty", required=True, type=float, help="Quantity")

    # Limit Order
    limit_parser = subparsers.add_parser("limit", help="Place Limit Order")
    limit_parser.add_argument("--symbol", required=True, help="Trading Pair")
    limit_parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    limit_parser.add_argument("--qty", required=True, type=float)
    limit_parser.add_argument("--price", required=True, type=float, help="Limit Price")

    # Stop Limit
    stop_parser = subparsers.add_parser("stop_limit", help="Place Stop-Limit Order")
    stop_parser.add_argument("--symbol", required=True)
    stop_parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    stop_parser.add_argument("--qty", required=True, type=float)
    stop_parser.add_argument("--price", required=True, type=float, help="Limit Price")
    stop_parser.add_argument("--stop_price", required=True, type=float, help="Trigger Price")

    # OCO
    oco_parser = subparsers.add_parser("oco", help="Place OCO Order (TP + SL)")
    oco_parser.add_argument("--symbol", required=True)
    oco_parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    oco_parser.add_argument("--qty", required=True, type=float)
    oco_parser.add_argument("--price", required=True, type=float, help="Take Profit Price")
    oco_parser.add_argument("--stop_price", required=True, type=float, help="Stop Loss Trigger")
    oco_parser.add_argument("--stop_limit_price", required=True, type=float, help="Stop Loss Limit Price")

    # TWAP
    twap_parser = subparsers.add_parser("twap", help="Execute TWAP Strategy")
    twap_parser.add_argument("--symbol", required=True)
    twap_parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    twap_parser.add_argument("--qty", required=True, type=float, help="Total Quantity")
    twap_parser.add_argument("--duration", required=True, type=int, help="Duration in seconds")
    twap_parser.add_argument("--orders", required=True, type=int, help="Number of slices")

    # Grid
    grid_parser = subparsers.add_parser("grid", help="Place Grid Orders")
    grid_parser.add_argument("--symbol", required=True)
    grid_parser.add_argument("--lower", required=True, type=float, help="Lower Price Range")
    grid_parser.add_argument("--upper", required=True, type=float, help="Upper Price Range")
    grid_parser.add_argument("--levels", required=True, type=int, help="Number of Grid Levels")
    grid_parser.add_argument("--qty_per_grid", required=True, type=float, help="Quantity per order")

    # Parse
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    logger.info(f"Command Received: {args.command}")

    try:
        if args.command == "market":
            place_market_order(args.symbol, args.side, args.qty)
        elif args.command == "limit":
            place_limit_order(args.symbol, args.side, args.qty, args.price)
        elif args.command == "stop_limit":
            place_stop_limit_order(args.symbol, args.side, args.qty, args.price, args.stop_price)
        elif args.command == "oco":
            place_oco_order(args.symbol, args.side, args.qty, args.price, args.stop_price, args.stop_limit_price)
        elif args.command == "twap":
            execute_twap(args.symbol, args.side, args.qty, args.duration, args.orders)
        elif args.command == "grid":
            execute_grid_strategy(args.symbol, args.lower, args.upper, args.levels, args.qty_per_grid)
            
    except Exception as e:
        logger.error(f"Execution Error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
