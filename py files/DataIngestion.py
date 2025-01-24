import yfinance as yf
import os
import pandas as pd

# List of stocks in the Magnificent Seven
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]

# Directory to save the CSV files
output_dir = "stock_data"
os.makedirs(output_dir, exist_ok=True)

# Function to clean and save the data
def save_cleaned_data(data, stock, output_path):
    # Reset index to make 'Date' a column
    data.reset_index(inplace=True)
    # Ensure the order of columns is consistent
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
    # Add the 'Ticker' column for clarity
    data["Ticker"] = stock
    # Save to CSV without extra indices or formatting issues
    data.to_csv(output_path, index=False)
    data = pd.read_csv(f'{output_path}')
    data = data.iloc[1:]
    data.to_csv(output_path, index=False)

# Download and save data for each stock
for stock in stocks:
    data = yf.download(stock, start="2015-01-01", end="2025-01-01")
    output_path = os.path.join(output_dir, f"{stock}.csv")
    save_cleaned_data(data, stock, output_path)