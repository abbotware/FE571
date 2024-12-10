import requests
import pandas as pd
import yfinance as yf
import datetime

# Define the sector ETFs
sector_etfs = {
    "XLF": "Financials",
    "XLK": "Technology",
    "XLE": "Energy",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLV": "Health Care",
    "XLI": "Industrials",
    "XLU": "Utilities",
    "XLRE": "Real Estate",
    "XLB": "Materials",
    "XLC": "Communication Services",
    "SPY": "S&P 500"
}

# Start and end dates for the data
start_date = datetime.datetime(2012, 1, 1)
end_date = datetime.datetime.today()

# Download daily prices for all sector ETFs
etf_data = {}
for etf, sector in sector_etfs.items():
    print(f"Downloading data for {sector} ({etf})...")
    etf_data[etf] = yf.download(etf, start=start_date, end=end_date)["Adj Close"]

# Combine all ETF data into a single DataFrame
etf_prices = pd.DataFrame(etf_data)

# Download risk-free rate (3-month Treasury Bill) from FRED via API
print("Downloading risk-free rate data...")
fred_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=TB3MS"
response = requests.get(fred_url)
with open("risk_free_rate_raw.csv", "wb") as f:
    f.write(response.content)

# Load risk-free rate data into pandas
rf_data = pd.read_csv("risk_free_rate_raw.csv", parse_dates=["DATE"])
rf_data.rename(columns={"DATE": "Date", "TB3MS": "Risk-Free Rate"}, inplace=True)
rf_data.set_index("Date", inplace=True)

# Save data to CSV files
etf_prices.to_csv("sector_etf_prices.csv", index_label="Date")
rf_data.to_csv("risk_free_rate.csv", index_label="Date")

print("Data download complete. Files saved as 'sector_etf_prices.csv' and 'risk_free_rate.csv'.")