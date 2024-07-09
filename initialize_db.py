import sqlite3

def initialize_db():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    
    # Drop the existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS stock_data')
    
    # Create the table again with new columns for percent change and average percent change
    cursor.execute('''
    CREATE TABLE stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        name TEXT NOT NULL,
        ticker_symbol TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        percent_change REAL,
        avg_percent_change REAL,
        UNIQUE(ticker_symbol, date)
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
