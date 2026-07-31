from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import load_data

def main():
    print("=" * 50)
    print("ETL PIPELINE - FASHION STUDIO")
    print("=" * 50)
    
    # 1. Extract
    print("\n[1/3] EXTRACT: Mengambil data dari website...")
    raw_data = scrape_main(max_pages=50)
    
    if raw_data is None or raw_data.empty:
        print("Extraction failed! Pipeline berhenti.")
        return
    
    print(f" Extract berhasil: {len(raw_data)} produk")
    
    # 2. Transform
    print("\n[2/3] TRANSFORM: Membersihkan data...")
    clean_data = transform_data(raw_data)
    
    if clean_data is None or clean_data.empty:
        print("Transform failed! Pipeline berhenti.")
        return
    
    print(f" Transform berhasil: {len(clean_data)} produk bersih")
    
    # 3. Load
    print("\n[3/3] LOAD: Menyimpan data ke CSV...")
    success = load_data(clean_data, "products.csv")
    
    if success:
        print("\n" + "=" * 50)
        print(" ETL PIPELINE SELESAI!")
        print(f" Output: products.csv ({len(clean_data)} rows)")
        print("=" * 50)
    else:
        print("\n Load failed!")

if __name__ == "__main__":
    main()