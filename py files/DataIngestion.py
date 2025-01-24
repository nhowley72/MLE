import pandas as pd 
import yfinance as yf # stock data here
import os 
from datetime import datetime

tikrs = ['AAPL', 'MSFT','AMZN','GOOG','TSLA','NVDA','META']
start_date = '2015-01-01'
end_date = datetime.now().strftime("%Y-%m-%d")
data_dir = "./stock_data"

# use the os package to make a folder just because we can! 
os.makedirs(data_dir, exist_ok=True)
def download_stock_data(stock, start_date, end_date):
    data = yf.download(stock, start=start_date, end=end_date)
    file_path = os.path.join(data_dir, f"{stock}.csv")
    data.to_csv(file_path)
    print(f"Saved {stock} data to {file_path}")

# Download Data for Each Stock
for stock in tikrs:
    download_stock_data(stock, start_date, end_date)