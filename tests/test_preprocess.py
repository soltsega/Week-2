import unittest
import pandas as pd
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))
from preprocess import clean_text, preprocess_data

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Sample test data
        self.sample_data = {
            'review_id': [1, 2, 3, 4],
            'review': ['Great!', '   ', 'Bad', None],
            'rating': [5, 3, 6, 4],
            'date': ['2025-01-01', '2025-01-02', 'invalid', '2025-01-03']
        }
        
    def test_clean_text(self):
        self.assertEqual(clean_text('  Hello  '), 'Hello')
        self.assertEqual(clean_text(None), '')
        self.assertEqual(clean_text(''), '')
        
    def test_preprocess_data(self):
        df = pd.DataFrame(self.sample_data)
        result = preprocess_data(df, 'test')
        
        # Should have 2 valid rows (one had empty review, one had invalid rating)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), 
                        ['review', 'rating', 'date', 'bank', 'source'])
        self.assertEqual(result['bank'].iloc[0], 'TEST')
        
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()