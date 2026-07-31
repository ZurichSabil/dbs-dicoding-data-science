import pandas as pd

def save_to_csv(df, filename="products.csv"):
    """Menyimpan DataFrame ke file CSV"""
    try:
        if df is None or df.empty:
            print("No data to save")
            return False
        
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
        print(f"Total rows saved: {len(df)}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

def load_data(df, csv_filename="products.csv"):
    """Fungsi utama loading data"""
    return save_to_csv(df, csv_filename)