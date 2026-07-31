import unittest
from unittest.mock import Mock, patch
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import scrape_main

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.get')
    def test_scrape_main_returns_dataframe(self, mock_get):
        # Mock response HTML
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="collection-card">
                <h3 class="product-title">T-shirt 2</h3>
                <span class="price">$100.00</span>
                <p>Rating: 4.8 / 5</p>
                <p style="font-size: 14px">5 Colors</p>
                <p style="font-size: 14px">Size: M</p>
                <p style="font-size: 14px">Gender: Men</p>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        df = scrape_main(max_pages=1)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreaterEqual(len(df), 0)
    
    @patch('utils.extract.requests.get')
    def test_columns_exist(self, mock_get):
        # Mock response HTML
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <div class="collection-card">
                <h3 class="product-title">T-shirt 2</h3>
                <span class="price">$100.00</span>
                <p>Rating: 4.8 / 5</p>
                <p style="font-size: 14px">5 Colors</p>
                <p style="font-size: 14px">Size: M</p>
                <p style="font-size: 14px">Gender: Men</p>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        
        df = scrape_main(max_pages=1)
        expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        for col in expected_columns:
            self.assertIn(col, df.columns)

if __name__ == "__main__":
    unittest.main()