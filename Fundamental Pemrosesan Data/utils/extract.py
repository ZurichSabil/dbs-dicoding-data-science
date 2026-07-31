import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

def scrape_main(base_url="https://fashion-studio.dicoding.dev", max_pages=50):
    products = []
    timestamp = datetime.now().isoformat()
    
    for page in range(1, max_pages + 1):
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}/page{page}"
        
        print(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            cards = soup.find_all('div', class_='collection-card')
            
            if not cards:
                print(f"No products found on page {page}, stopping...")
                break
            
            for card in cards:
                try:
                    # Title
                    title_elem = card.find('h3', class_='product-title')
                    title = title_elem.text.strip() if title_elem else "Unknown Product"
                    
                    # Price
                    price_elem = card.find('span', class_='price')
                    if price_elem:
                        price = price_elem.text.strip()
                    else:
                        price_para = card.find('p', string=re.compile(r'\$'))
                        price = price_para.text.strip() if price_para else "Price Unavailable"
                    
                    # Rating
                    rating_elem = card.find('p', string=re.compile(r'Rating:'))
                    rating = rating_elem.text.strip() if rating_elem else "Rating: Invalid Rating / 5"
                    
                    # Detail: Colors, Size, Gender
                    detail_paras = card.find_all('p', style=re.compile(r'font-size: 14px'))
                    colors = "0 Colors"
                    size = "Size: Unknown"
                    gender = "Gender: Unknown"
                    
                    for p in detail_paras:
                        text = p.text.strip()
                        if 'Colors' in text or 'colors' in text:
                            colors = text
                        elif 'Size:' in text:
                            size = text
                        elif 'Gender:' in text:
                            gender = text
                    
                    # Jika size/gender tidak ditemukan, cari di tempat lain
                    if size == "Size: Unknown":
                        size_elem = card.find('p', string=re.compile(r'Size:'))
                        size = size_elem.text.strip() if size_elem else "Size: Unknown"
                    
                    if gender == "Gender: Unknown":
                        gender_elem = card.find('p', string=re.compile(r'Gender:'))
                        gender = gender_elem.text.strip() if gender_elem else "Gender: Unknown"
                    
                    products.append({
                        'Title': title,
                        'Price': price,
                        'Rating': rating,
                        'Colors': colors,
                        'Size': size,
                        'Gender': gender,
                        'Timestamp': timestamp
                    })
                except Exception as e:
                    print(f"Error parsing product card: {e}")
                    continue
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            continue
    
    print(f"Scraping completed. Total products: {len(products)}")
    return pd.DataFrame(products)

if __name__ == "__main__":
    df = scrape_main(max_pages=2)
    print("\nPreview data:")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")