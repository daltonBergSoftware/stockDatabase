import yfinance as yf
import sqlite3
from datetime import datetime, timedelta

def fetch_and_store_stock_data(symbols):
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    
    # Define the date range
    start_date = '2024-07-01'
    end_date = '2024-07-09'  # We need to go one day past to include July 8th

    for symbol, name in symbols.items():
        print(f"Fetching data for {name} ({symbol})")
        # Fetch the data
        data = yf.download(symbol, start=start_date, end=end_date)
        
        if not data.empty:
            total_percent_change = 0
            num_days = 0

            for date in data.index:
                date_str = date.strftime('%Y-%m-%d')
                day_data = data.loc[date]
                open_price = day_data['Open']
                close_price = day_data['Close']
                high_price = day_data['High']
                low_price = day_data['Low']

                # Calculate percent change from open to close
                percent_change = ((close_price - open_price) / open_price) * 100

                # Update the total percent change and number of days
                total_percent_change += percent_change
                num_days += 1
                avg_percent_change = total_percent_change / num_days

                # Insert the data into the SQLite database
                cursor.execute('''
                    INSERT OR IGNORE INTO stock_data (date, name, ticker_symbol, open_price, close_price, high_price, low_price, percent_change, avg_percent_change)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date_str,
                    name,                 # Company name
                    symbol,               # Ticker symbol
                    open_price,           # Open price
                    close_price,          # Close price
                    high_price,           # High price
                    low_price,            # Low price
                    percent_change,       # Percent change
                    avg_percent_change    # Average percent change
                ))

            print(f"Data for {name} ({symbol}) has been inserted into the database.")
        else:
            print(f"No data available for {name} ({symbol}) in the specified date range.")

    conn.commit()  # Commit the changes to the database
    conn.close()   # Close the database connection

def main():
    symbols = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'AMZN': 'Amazon.com Inc.',
        'META': 'Meta Platforms Inc.'  # Updated ticker symbol for Meta
    }
    fetch_and_store_stock_data(symbols)

if __name__ == '__main__':
    main()
