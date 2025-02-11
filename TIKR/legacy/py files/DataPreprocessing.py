import os
import pandas as pd

# Directory where stock data CSV files are stored
data_dir = "stock_data"
output_dir = "processed_stock_data"
os.makedirs(output_dir, exist_ok=True)

# Function to preprocess data for each stock
def preprocess_stock_data(file_path):
    # Load the stock data
    data = pd.read_csv(file_path)
    
    # Ensure the Date column is a datetime object
    data["Date"] = pd.to_datetime(data["Date"])
    data.sort_values(by="Date", inplace=True)
    
    # Create new columns
    data["Daily Return"] = data["Close"].pct_change()  # Daily percentage return
    data["5-Day Moving Avg"] = data["Close"].rolling(window=5).mean()  # 5-day moving average
    data["10-Day Volatility"] = data["Close"].rolling(window=10).std()  # 10-day rolling standard deviation (volatility)
    
    # Drop rows with NaN values caused by rolling calculations
    data.dropna(inplace=True)
    
    return data

# Process and save each stock's data
for file_name in os.listdir(data_dir):
    if file_name.endswith(".csv"):
        stock_file_path = os.path.join(data_dir, file_name)
        stock_name = os.path.splitext(file_name)[0]
        print(f"Processing data for {stock_name}...")
        
        # Preprocess the data
        processed_data = preprocess_stock_data(stock_file_path)
        
        # Save the processed data
        output_path = os.path.join(output_dir, f"{stock_name}_processed.csv")
        processed_data.to_csv(output_path, index=False)
        print(f"Saved processed data for {stock_name} to {output_path}")

print("Data preprocessing complete!")
