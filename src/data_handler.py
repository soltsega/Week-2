import pandas as pd
import emoji
import time
from typing import List, Dict, Any, Tuple, Optional
from deep_translator import GoogleTranslator
from config.settings import TRANSLATION_CONFIG, EMOJI_CONFIG, VALIDATION

def create_output_dir(dir_name: str = 'data') -> None:
    """Create output directory if it doesn't exist."""
    import os
    os.makedirs(dir_name, exist_ok=True)

def translate_text(text: str, target_lang: str = 'en') -> str:
    """Translate text to target language with retry logic."""
    if not text or not text.strip() or len(text) < VALIDATION['min_review_length']:
        return text
        
    for attempt in range(TRANSLATION_CONFIG['retries']):
        try:
            return GoogleTranslator(
                source='auto',
                target=target_lang,
                timeout=TRANSLATION_CONFIG['timeout']
            ).translate(text)
        except Exception as e:
            if attempt == TRANSLATION_CONFIG['retries'] - 1:
                print(f"Translation failed after {TRANSLATION_CONFIG['retries']} attempts: {e}")
                return text
            time.sleep(1)  # Wait before retry

def extract_emoji_info(text: str) -> Dict[str, Any]:
    """Extract emoji information from text."""
    if not isinstance(text, str):
        return {'emojis': [], 'count': 0, 'descriptions': []}
    
    emoji_chars = [c for c in text if c in emoji.EMOJI_DATA]
    emoji_descriptions = [emoji.demojize(e) for e in emoji_chars]
    
    return {
        'emojis': emoji_chars,
        'count': len(emoji_chars),
        'descriptions': emoji_descriptions
    }

def process_reviews(raw_reviews: List[Dict[str, Any]], bank_name: str) -> List[Dict[str, Any]]:
    """Process and clean review data."""
    processed = []
    
    for review in raw_reviews:
        content = review.get('content', '')
        language = review.get('language', 'en')
        
        # Skip if review is too short
        if len(str(content).strip()) < VALIDATION['min_review_length']:
            continue
            
        # Extract emoji information
        emoji_info = extract_emoji_info(content) if EMOJI_CONFIG['extract_emojis'] else {
            'emojis': [], 'count': 0, 'descriptions': []
        }
        
        # Translate if enabled and needed
        translated_content = ""
        if (TRANSLATION_CONFIG['enabled'] and 
            language != TRANSLATION_CONFIG['target_language'] and 
            content.strip()):
            translated_content = translate_text(content, TRANSLATION_CONFIG['target_language'])
        
        # Build review data
        review_data = {
            'review_id': review.get('reviewId', ''),
            'bank': bank_name,
            'app_id': review.get('app_id', ''),
            'review': content,
            'review_clean': emoji.replace_emoji(str(content), replace='').strip(),
            'rating': min(max(int(review.get('score', 0)), 1), 5),  # Ensure 1-5
            'date': review.get('at', '').strftime('%Y-%m-%d') if review.get('at') else '',
            'thumbs_up': int(review.get('thumbsUpCount', 0)),
            'language': language,
            'scrape_timestamp': review.get('scrape_timestamp', ''),
            'translated_review': translated_content if translated_content else content,
            'is_translated': bool(translated_content and language != TRANSLATION_CONFIG['target_language']),
            **{k: v for k, v in zip(
                EMOJI_CONFIG['emoji_columns'].values(),
                [emoji_info['emojis'], emoji_info['count'], emoji_info['descriptions']]
            )}
        }
        
        processed.append(review_data)
    
    return processed

def save_to_csv(data: List[Dict[str, Any]], filename: str) -> bool:
    """Save processed data to CSV with error handling."""
    if not data:
        print("No data to save!")
        return False
    
    try:
        df = pd.DataFrame(data)
        
        # Ensure all expected columns exist
        expected_columns = [
            'review_id', 'bank', 'app_id', 'review', 'review_clean', 'rating',
            'date', 'thumbs_up', 'language', 'scrape_timestamp',
            'translated_review', 'is_translated'
        ]
        
        # Add emoji columns if enabled
        if EMOJI_CONFIG['extract_emojis']:
            expected_columns.extend(EMOJI_CONFIG['emoji_columns'].values())
        
        # Add missing columns with default values
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
        
        # Reorder columns
        df = df[expected_columns]
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ Saved {len(df)} reviews to {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving to {filename}: {e}")
        return False