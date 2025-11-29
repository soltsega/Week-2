import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('preprocessing.log')
    ]
)
logger = logging.getLogger(__name__)

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load and validate the input CSV file."""
    try:
        df = pd.read_csv(file_path)
        required_columns = ['review_id', 'review', 'rating', 'date']
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            logger.error(f"Missing required columns: {', '.join(missing)}")
            return None
        return df
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}")
        return None

def clean_text(text: str) -> str:
    """Clean and normalize review text."""
    if pd.isna(text):
        return ""
    return str(text).strip()

def preprocess_data(df: pd.DataFrame, bank_name: str) -> pd.DataFrame:
    """Clean and preprocess the review data."""
    # 1. Remove duplicates
    df = df.drop_duplicates(subset=['review_id'])
    
    # 2. Clean review text
    df['review'] = df['review'].apply(clean_text)
    df = df[df['review'] != '']
    
    # 3. Validate and clean ratings
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df[df['rating'].between(1, 5)]
    
    # 4. Clean and format dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    
    # 5. Add metadata
    df['bank'] = bank_name.upper()
    df['source'] = 'Google Play Store'
    
    # 6. Select and order columns
    columns = ['review', 'rating', 'date', 'bank', 'source']
    return df[columns]

def save_processed_data(df: pd.DataFrame, output_path: str) -> bool:
    """Save the processed data to CSV."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        return True
    except Exception as e:
        logger.error(f"Error saving to {output_path}: {str(e)}")
        return False

def process_bank(input_file: str, output_file: str) -> Dict:
    """Process a single bank's data."""
    bank_name = Path(input_file).stem.split('_')[-1]
    logger.info(f"\nProcessing {bank_name.upper()}...")
    
    # Load and validate data
    df = load_data(input_file)
    if df is None:
        return {'bank': bank_name, 'status': 'failed', 'reason': 'load_error'}
    
    initial_count = len(df)
    
    # Preprocess data
    processed_df = preprocess_data(df, bank_name)
    final_count = len(processed_df)
    
    # Save results
    if save_processed_data(processed_df, output_file):
        return {
            'bank': bank_name.upper(),
            'status': 'success',
            'initial_rows': initial_count,
            'final_rows': final_count,
            'duplicates_removed': initial_count - final_count
        }
    return {'bank': bank_name, 'status': 'failed', 'reason': 'save_error'}

def main():
    """Main function to run the preprocessing pipeline."""
    # Set up paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir.parent / 'data'  # Changed: Now points to Week-2/data
    output_dir = data_dir / 'processed'
    
    # Process each bank
    bank_files = [
        'bank_reviews_cbe.csv',
        'bank_reviews_boa.csv',
        'bank_reviews_dashen.csv'
    ]
    
    results = []
    for bank_file in bank_files:
        input_path = data_dir / bank_file
        output_path = output_dir / f"cleaned_{bank_file}"
        result = process_bank(str(input_path), str(output_path))
        results.append(result)
    
    # Print summary
    logger.info("\n=== Processing Summary ===")
    for result in results:
        if result['status'] == 'success':
            logger.info(
                f"{result['bank']}: {result['final_rows']} reviews "
                f"({result['duplicates_removed']} rows removed)"
            )
        else:
            logger.error(f"{result['bank']}: Failed - {result.get('reason', 'unknown')}")

if __name__ == "__main__":
    main()