import pandas as pd
import re

def convert_price_to_idr(price_str):
    try:
        if pd.isna(price_str) or price_str == "Price Unavailable":
            return None
        match = re.search(r'\$([\d,]+\.?\d*)', str(price_str))
        if match:
            usd = float(match.group(1).replace(',', ''))
            return usd * 16000
        return None
    except:
        return None

def clean_rating(rating_str):
    try:
        if pd.isna(rating_str):
            return None
        if "Invalid" in str(rating_str) or "Not Rated" in str(rating_str):
            return None
        match = re.search(r'(\d+\.?\d*)\s*/\s*\d+', str(rating_str))
        if match:
            return float(match.group(1))
        return None
    except:
        return None

def clean_colors(colors_str):
    try:
        if pd.isna(colors_str):
            return None
        match = re.search(r'(\d+)\s*Colors?', str(colors_str), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    except:
        return None

def clean_size(size_str):
    try:
        if pd.isna(size_str):
            return None
        return re.sub(r'^Size:\s*', '', str(size_str), flags=re.IGNORECASE).strip()
    except:
        return None

def clean_gender(gender_str):
    try:
        if pd.isna(gender_str):
            return None
        return re.sub(r'^Gender:\s*', '', str(gender_str), flags=re.IGNORECASE).strip()
    except:
        return None

def transform_data(df):
    if df is None or df.empty:
        print("No data to transform")
        return None
    
    df_clean = df.copy()
    
    print(f"Original data: {len(df_clean)} rows")
    
    # Bersihkan spasi berlebih di Title
    df_clean['Title'] = df_clean['Title'].str.strip()
    
    # Hapus produk yang mengandung "Unknown"
    before_unknown = len(df_clean)
    df_clean = df_clean[~df_clean['Title'].str.contains('Unknown', case=False, na=False)]
    print(f"After removing Unknown Product: {len(df_clean)} rows (removed {before_unknown - len(df_clean)})")
    
    # Konversi Price ke Rupiah
    df_clean['Price'] = df_clean['Price'].apply(convert_price_to_idr)
    
    # Bersihkan kolom lainnya
    df_clean['Rating'] = df_clean['Rating'].apply(clean_rating)
    df_clean['Colors'] = df_clean['Colors'].apply(clean_colors)
    df_clean['Size'] = df_clean['Size'].apply(clean_size)
    df_clean['Gender'] = df_clean['Gender'].apply(clean_gender)
    
    # Hapus produk dengan rating invalid ATAU harga kosong
    before_clean = len(df_clean)
    df_clean = df_clean[df_clean['Rating'].notna() & df_clean['Price'].notna()]
    print(f"After removing invalid rating & no price: {len(df_clean)} rows (removed {before_clean - len(df_clean)})")
    
    # Reset index
    df_clean = df_clean.reset_index(drop=True)
    
    # Ubah tipe data Title, Size, Gender menjadi object
    df_clean['Title'] = df_clean['Title'].astype('object')
    df_clean['Size'] = df_clean['Size'].astype('object')
    df_clean['Gender'] = df_clean['Gender'].astype('object')
    
    print("Transformation completed!")
    return df_clean