from google_play_scraper import app, reviews_all, Sort
from tqdm import tqdm
import time
from typing import Dict, List, Optional, Any
from config.settings import SCRAPING_CONFIG, LANGUAGE_CONFIG

def get_app_info(app_id: str, lang: str = 'en') -> Optional[Dict[str, Any]]:
    """Fetch basic app information from Google Play Store."""
    try:
        app_info = app(app_id, lang=lang)
        return {
            'title': app_info.get('title', ''),
            'score': app_info.get('score', 0),
            'installs': app_info.get('installs', ''),
            'version': app_info.get('version', ''),
            'updated': app_info.get('updated', '')
        }
    except Exception as e:
        print(f"Error fetching app info ({lang}): {e}")
        return None

def scrape_app_reviews(
    app_id: str,
    count: int = 100,
    languages: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Scrape reviews for a specific app in multiple languages.
    
    Args:
        app_id: The app's package name
        count: Number of reviews per language
        languages: List of language codes to scrape
        
    Returns:
        List of review dictionaries with language information
    """
    if languages is None:
        languages = [LANGUAGE_CONFIG['default_language']]
        
    all_reviews = []
    
    for lang in languages:
        try:
            print(f"  - Scraping {lang.upper()} reviews...")
            
            reviews = reviews_all(
                app_id,
                sleep_milliseconds=1000,
                lang=lang,
                country=SCRAPING_CONFIG['country'],
                sort=Sort.MOST_RELEVANT,
                count=count
            )
            
            # Add language and timestamp to each review
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            for review in reviews:
                review.update({
                    'language': lang,
                    'scrape_timestamp': timestamp,
                    'app_id': app_id
                })
                
            all_reviews.extend(reviews)
            print(f"  ✓ Found {len(reviews)} {lang.upper()} reviews")
            
        except Exception as e:
            print(f"  ✗ Error scraping {lang.upper()} reviews: {e}")
            continue
                    
    return all_reviews