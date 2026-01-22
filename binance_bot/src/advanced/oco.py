from src.client import BinanceClient
from src.utils import logger, validate_inputs
import config

def place_oco_order(symbol, side, qty, price, stop_price, stop_limit_price):
    """
    Simulates an OCO (One-Cancels-the-Other) order for Futures.
    Note: Binance Futures does not have a native single 'OCO' endpoint like Spot.
    Typically achieved by placing two orders:
    1. Limit Order (Take Profit)
    2. Stop Market/Limit Order (Stop Loss)
    
    This function places BOTH. (Note: Cancelling one when other fills requires WebSocket monitoring, 
    unavailable in this simple CLI. We just place both legs here).
    """
    try:
        validate_inputs(symbol, side, qty, price)
        
        client = BinanceClient(config.API_KEY, config.API_SECRET, config.BASE_URL)
        
        logger.info(f"Placing OCO Strategy for {symbol} {side} {qty}")
        
        # 1. Limit Order (Take Profit)
        # If side is BUY, TP is SELL at higher price.
        # If side is SELL, TP is BUY at lower price.
        # This assumes we are entering a position or closing one. 
        # For simplicity, we assume we are OPENING a position with this OCO? 
        # OR we are SETTING TP/SL for an existing position?
        # Standard OCO usage: Buy Limit + Buy Stop (to enter) OR Sell Limit + Sell Stop (to exit).
        
        # Let's assume exiting a position (ReduceOnly = True usually preferable).
        
        # Leg 1: Take Profit (Limit)
        params_tp = {
            'symbol': symbol,
            'side': side.upper(),
            'type': 'LIMIT',
            'quantity': qty,
            'price': price,
            'timeInForce': 'GTC'
        }
        
        # Leg 2: Stop Loss (Stop Limit)
        params_sl = {
            'symbol': symbol,
            'side': side.upper(),
            'type': 'STOP',
            'quantity': qty,
            'price': stop_limit_price,
            'stopPrice': stop_price,
            'timeInForce': 'GTC'
        }
        
        # Use Batch Orders if possible for atomicity
        endpoint = "/fapi/v1/batchOrders"
        import json
        batch_params = {
            'batchOrders': json.dumps([params_tp, params_sl])
        }
        
        logger.info(f"Sending Batch OCO: TP @ {price}, SL @ {stop_price}")
        response = client.send_request('POST', endpoint, batch_params)
        
        logger.info(f"OCO Orders Placed. Responses: {len(response)}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to place OCO order: {e}")
        return None
