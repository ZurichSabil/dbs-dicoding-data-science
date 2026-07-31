import unittest
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import convert_price_to_idr, clean_rating, clean_colors, clean_size, clean_gender, transform_data

class TestTransform(unittest.TestCase):
    
    def test_convert_price_to_idr(self):
        self.assertEqual(convert_price_to_idr("$100.00"), 1600000)
        self.assertEqual(convert_price_to_idr("$50.50"), 808000)
        self.assertIsNone(convert_price_to_idr("Price Unavailable"))
    
    def test_clean_rating(self):
        self.assertEqual(clean_rating("Rating: 4.8 / 5"), 4.8)
        self.assertIsNone(clean_rating("Invalid Rating"))
    
    def test_clean_colors(self):
        self.assertEqual(clean_colors("5 Colors"), 5)
        self.assertEqual(clean_colors("3 colors"), 3)
    
    def test_clean_size(self):
        self.assertEqual(clean_size("Size: M"), "M")
        self.assertEqual(clean_size("Size: XL"), "XL")
    
    def test_clean_gender(self):
        self.assertEqual(clean_gender("Gender: Men"), "Men")
        self.assertEqual(clean_gender("Gender: Women"), "Women")
    
    def test_transform_data(self):
        data = {
            'Title': ['T-shirt 2', 'Unknown Product'],
            'Price': ['$100.00', 'Price Unavailable'],
            'Rating': ['Rating: 4.8 / 5', 'Invalid Rating'],
            'Colors': ['5 Colors', '3 Colors'],
            'Size': ['Size: M', 'Size: L'],
            'Gender': ['Gender: Men', 'Gender: Women'],
            'Timestamp': ['2025-01-01', '2025-01-01']
        }
        df = pd.DataFrame(data)
        result = transform_data(df)
        self.assertEqual(len(result), 1)

if __name__ == "__main__":
    unittest.main()