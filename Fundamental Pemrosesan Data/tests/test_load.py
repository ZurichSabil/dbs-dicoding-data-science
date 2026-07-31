import unittest
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import save_to_csv

class TestLoad(unittest.TestCase):
    
    def test_save_to_csv_success(self):
        test_df = pd.DataFrame({'Test': [1, 2, 3]})
        filename = "test_output.csv"
        result = save_to_csv(test_df, filename)
        self.assertTrue(result)
        
        # Bersihkan file test
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()