import time
from src.client import BinanceClient
from src.utils import logger, validate_inputs
import config

def execute_twap(symbol, side, total_qty, duration_seconds, num_orders):
    """
    Executes a TWAP (Time Weighted Average Price) strategy.
    Splits total_qty into num_orders and executes them over duration_seconds.
    """
    try:
        validate_inputs(symbol, side, total_qty)
        
        if duration_seconds <= 0 or num_orders <= 0:
            raise ValueError("Duration and Order Count must be positive.")
            
        qty_per_order = round(total_qty / num_orders, 3) # Adjust precision logic for real usage
        interval = duration_seconds / num_orders
        
        client = BinanceClient(config.API_KEY, config.API_SECRET, config.BASE_URL)
        
        logger.info(f"Starting TWAP: {side} {total_qty} {symbol} over {duration_seconds}s in {num_orders} slices.")
        
        for i in range(num_orders):
            logger.info(f"TWAP Slice {i+1}/{num_orders}: Placing Market Order for {qty_per_order}")
            
            # Place Market Order slice
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'MARKET',
                'quantity': qty_per_order
            }
            
            # Fire and log
            try:
                resp = client.send_request('POST', "/fapi/v1/order", params)
                logger.info(f"Slice {i+1} Filled: {resp.get('orderId', 'Unknown ID')}")
            except Exception as slice_err:
                logger.error(f"Slice {i+1} Failed: {slice_err}")
                # Continue strategy even if one fails? Yes, usually.
            
            if i < num_orders - 1:
                logger.info(f"Sleeping for {interval:.2f}s...")
                time.sleep(interval)
                
        logger.info("TWAP Strategy Completed.")
        return True
        
    except Exception as e:
        logger.error(f"TWAP Strategy Failed: {e}")
        return False
