from src.client import BinanceClient
from src.utils import logger, validate_inputs
import config
import json

def execute_grid_strategy(symbol, lower_price, upper_price, grid_levels, qty_per_grid):
    """
    Places a simple Grid of Limit Orders (Long/Short) within a range.
    Note: Real grid bots are dynamic. This is a static 'Place Orders' setup.
    """
    try:
        client = BinanceClient(config.API_KEY, config.API_SECRET, config.BASE_URL)
        
        price_step = (upper_price - lower_price) / (grid_levels - 1)
        
        orders = []
        
        current_price_info = client.send_request('GET', '/fapi/v1/ticker/price', {'symbol': symbol})
        current_price = float(current_price_info['price'])
        
        logger.info(f"Grid Strategy: Range [{lower_price} - {upper_price}], Current: {current_price}")
        
        for i in range(grid_levels):
            price = lower_price + (i * price_step)
            price = round(price, 2) # Adjust precision
            
            # Simple Neutral Grid logic:
            # Below Market Price -> BUY
            # Above Market Price -> SELL
            
            if price < current_price:
                side = 'BUY'
            else:
                side = 'SELL'
                
            order = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': qty_per_grid,
                'price': str(price),
                'timeInForce': 'GTC'
            }
            orders.append(order)
            
        # Send Batch
        # Binance limits batch to 5 orders per request usually. We'll chunk it.
        chunk_size = 5
        for i in range(0, len(orders), chunk_size):
            chunk = orders[i:i + chunk_size]
            logger.info(f"Placing Grid Batch {i//chunk_size + 1} ({len(chunk)} orders)...")
            
            params = {
                'batchOrders': json.dumps(chunk)
            }
            client.send_request('POST', "/fapi/v1/batchOrders", params)
            
        logger.info(f"Grid Strategy Placed {len(orders)} orders.")
        return True
        
    except Exception as e:
        logger.error(f"Grid Strategy Failed: {e}")
        return False
