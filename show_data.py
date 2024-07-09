import sqlite3

def print_sample_data():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock_data")  # Remove LIMIT to see all data
    rows = cursor.fetchall()
    print("Sample data from the database:")
    for row in rows:
        print(row)
    conn.close()

if __name__ == '__main__':
    print_sample_data()
