import pandas as pd
import matplotlib.pyplot as plt
import os
import data_loader

def generate_report(merged_df, output_dir):
    """
    Generates analysis report and visualizations.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert numeric columns just in case
    merged_df['Closed PnL'] = pd.to_numeric(merged_df['Closed PnL'], errors='coerce').fillna(0)
    merged_df['Size USD'] = pd.to_numeric(merged_df['Size USD'], errors='coerce').fillna(0)
    
    # Filter out rows with Missing Classification (if any)
    df = merged_df.dropna(subset=['classification'])
    
    report_lines = []
    report_lines.append("# Trader Behavior Analysis Report")
    report_lines.append(f"Total Trades Analyzed: {len(df)}")
    
    # 1. PnL by Sentiment
    pnl_stats = df.groupby('classification')['Closed PnL'].agg(['mean', 'sum', 'count', 'std'])
    report_lines.append("\n## PnL by Market Sentiment")
    report_lines.append(pnl_stats.to_string())
    
    # 2. Win Rate by Sentiment
    df['Win'] = df['Closed PnL'] > 0
    win_rate = df.groupby('classification')['Win'].mean()
    report_lines.append("\n## Win Rate by Market Sentiment")
    report_lines.append(win_rate.to_string())
    
    # 3. Volume by Sentiment
    volume_stats = df.groupby('classification')['Size USD'].agg(['mean', 'sum'])
    report_lines.append("\n## Volume (Size USD) by Market Sentiment")
    report_lines.append(volume_stats.to_string())
    
    # 4. Correlation Analysis
    # Map classification to ordinal if needed, or just use 'value' (0-100)
    corr_pnl = df['value'].corr(df['Closed PnL'])
    corr_vol = df['value'].corr(df['Size USD'])
    
    report_lines.append("\n## Correlation Analysis")
    report_lines.append(f"- **Fear/Greed Index vs PnL**: {corr_pnl:.4f}")
    report_lines.append(f"- **Fear/Greed Index vs Volume**: {corr_vol:.4f}")

    # 5. Top Trader (Whale) Analysis
    report_lines.append("\n## Top Trader 'Whale' Analysis")
    # Identify Top 5 Traders by Volume
    top_traders = df.groupby('Account')['Size USD'].sum().nlargest(5).index
    whales_df = df[df['Account'].isin(top_traders)]
    
    report_lines.append(f"Analyzing Top {len(top_traders)} Accounts by Volume.")
    
    # Whale Win Rate by Sentiment
    whale_win_rate = whales_df.groupby('classification')['Win'].mean()
    report_lines.append("\n### Whale Win Rate by Market Sentiment")
    report_lines.append(whale_win_rate.to_string())
    
    # Compare Whale vs All in Extreme Fear
    target_sentiment = 'Extreme Fear'
    if target_sentiment in df['classification'].values:
        fear_df = df[df['classification'] == target_sentiment]
        all_fear_win_rate = fear_df['Win'].mean()
        
        whale_fear_df = whales_df[whales_df['classification'] == target_sentiment]
        whale_fear_win_rate = whale_fear_df['Win'].mean() if len(whale_fear_df) > 0 else 0
        
        report_lines.append(f"\n### Performance in '{target_sentiment}'")
        report_lines.append(f"- **General Population Win Rate**: {all_fear_win_rate:.2%}")
        report_lines.append(f"- **Top Traders (Whales) Win Rate**: {whale_fear_win_rate:.2%}")
    else:
        report_lines.append(f"\n### Performance in '{target_sentiment}'")
        report_lines.append(f"- No trades occurred during '{target_sentiment}' periods in this dataset.")
    
    # Visualizations
    
    # Visualizations
    
    # Bar Chart: Avg PnL by Sentiment
    plt.figure(figsize=(10, 6))
    pnl_stats['mean'].plot(kind='bar', color='skyblue')
    plt.title('Average PnL by Market Sentiment')
    plt.ylabel('Average PnL (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'pnl_by_sentiment.png'))
    plt.close()

    # Bar Chart: Whale Win Rate
    plt.figure(figsize=(10, 6))
    whale_win_rate.plot(kind='bar', color='gold')
    plt.title('Whale Win Rate by Market Sentiment')
    plt.ylabel('Win Rate')
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'whale_win_rate.png'))
    plt.close()
    
    # Bar Chart: Win Rate by Sentiment
    plt.figure(figsize=(10, 6))
    win_rate.plot(kind='bar', color='lightgreen')
    plt.title('Win Rate by Market Sentiment')
    plt.ylabel('Win Rate')
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'win_rate_by_sentiment.png'))
    plt.close()
    
    # Scatter: Sentiment Value vs PnL (Sampled if too large)
    plt.figure(figsize=(10, 6))
    sample_df = df.sample(min(10000, len(df)))
    
    # Color by classification
    groups = sample_df.groupby('classification')
    for name, group in groups:
        plt.plot(group['value'], group['Closed PnL'], marker='o', linestyle='', label=name, alpha=0.6)

    plt.title('Fear/Greed Index vs PnL (Sampled 10k)')
    plt.xlabel('Fear/Greed Index (0=Fear, 100=Greed)')
    plt.ylabel('Closed PnL')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sentiment_vs_pnl.png'))
    plt.close()

    # Save Report
    with open(os.path.join(output_dir, 'report.md'), 'w') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Report generated at {os.path.join(output_dir, 'report.md')}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fg_path = os.path.join(base_dir, 'data', 'fear_greed_index.csv')
    trade_path = os.path.join(base_dir, 'data', 'historical_data.csv')
    
    print("Loading data...")
    try:
        fg = data_loader.load_fear_greed(fg_path)
        trades = data_loader.load_trade_data(trade_path)
        merged = data_loader.merge_datasets(trades, fg)
        
        print("Generating report...")
        generate_report(merged, base_dir)
        
    except Exception as e:
        print(f"Error: {e}")
