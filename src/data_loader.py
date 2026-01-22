import pandas as pd
import os

def load_fear_greed(filepath):
    """
    Loads Fear and Greed Index data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    # Convert 'date' to datetime
    df['date'] = pd.to_datetime(df['date'])
    # Normalize to date only (just in case)
    df['date'] = df['date'].dt.date
    return df

def load_trade_data(filepath):
    """
    Loads Historical Trader Data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    
    # Parse Timestamp. 'Timestamp' column seems to be in milliseconds.
    # We can also use 'Timestamp IST' if needed, but unix timestamp is safer.
    # However, looking at the preview, 'Timestamp' is float/scientific notation.
    
    # Let's try parsing 'Timestamp' as ms
    df['datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    
    # Create a 'date' column for merging
    df['date'] = df['datetime'].dt.date
    
    return df

def merge_datasets(trades_df, fear_greed_df):
    """
    Merges trades with fear/greed data on date.
    """
    # Merge on date
    # Fear Greed is daily, so we join on the 'date' column
    merged_df = pd.merge(trades_df, fear_greed_df, on='date', how='left')
    
    return merged_df

if __name__ == "__main__":
    # Test execution
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fg_path = os.path.join(base_dir, 'data', 'fear_greed_index.csv')
    trade_path = os.path.join(base_dir, 'data', 'historical_data.csv')
    
    print(f"Loading Fear/Greed from {fg_path}...")
    fg = load_fear_greed(fg_path)
    print(f"Loaded {len(fg)} rows.")
    
    print(f"Loading Trades from {trade_path}...")
    trades = load_trade_data(trade_path)
    print(f"Loaded {len(trades)} rows.")
    
    print("Merging...")
    merged = merge_datasets(trades, fg)
    print(f"Merged: {len(merged)} rows.")
    print("Sample:\n", merged[['date', 'value', 'classification', 'Closed PnL']].head())
