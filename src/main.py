import time
from typing import List, Dict, Any
from config.settings import BANK_APPS, SCRAPING_CONFIG, LANGUAGE_CONFIG, TRANSLATION_CONFIG
from src.scraper import get_app_info, scrape_app_reviews
from src.data_handler import process_reviews, save_to_csv, create_output_dir

def print_app_info(app_info: Dict[str, Any], bank_name: str) -> None:
    """Print formatted app information."""
    if not app_info:
        print(f"  Could not fetch app info for {bank_name}")
        return
        
    print(f"\n📱 {app_info['title']}")
    print(f"   ⭐ Rating: {app_info['score']:.1f} ★")
    print(f"   📥 Installs: {app_info['installs']}")
    print(f"   🔄 Version: {app_info.get('version', 'N/A')}")
    print(f"   📅 Last Updated: {app_info.get('updated', 'N/A')}")

def main():
    """Main function to orchestrate the scraping and processing of app reviews."""
    all_reviews = []
    create_output_dir(SCRAPING_CONFIG['output']['directory'])
    
    print("\n" + "="*60)
    print("🚀 Starting Bank App Review Scraper")
    print("="*60)
    print(f"📊 Target: {len(BANK_APPS)} banks")
    print(f"🌐 Languages: {', '.join(LANGUAGE_CONFIG['supported_languages'])}")
    if TRANSLATION_CONFIG['enabled']:
        print(f"🔄 Translation to {LANGUAGE_CONFIG['target_language'].upper()} is ENABLED")
    else:
        print("⏭️  Translation is DISABLED")
    print("="*60 + "\n")
    
    # Process each bank's app
    for bank_key, bank_data in BANK_APPS.items():
        app_id = bank_data['id']
        bank_name = bank_data['name']
        languages = bank_data.get('supported_languages', [LANGUAGE_CONFIG['default_language']])
        
        # Print header
        print("\n" + "="*60)
        print(f"🔍 Processing {bank_name} ({app_id})")
        print("="*60)
        
        # Get app info
        app_info = get_app_info(app_id, LANGUAGE_CONFIG['default_language'])
        print_app_info(app_info, bank_name)
        
        # Scrape reviews
        print(f"\n🔄 Scraping up to {SCRAPING_CONFIG['reviews_per_language']} reviews per language...")
        start_time = time.time()
        
        reviews = scrape_app_reviews(
            app_id=app_id,
            count=SCRAPING_CONFIG['reviews_per_language'],
            languages=languages
        )
        
        if reviews:
            # Process reviews
            print(f"\n🔄 Processing {len(reviews)} reviews...")
            processed = process_reviews(reviews, bank_name)
            all_reviews.extend(processed)
            
            # Print summary
            lang_counts = {}
            for r in processed:
                lang = r.get('language', 'unknown')
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
                
            print(f"✅ Processed {len(processed)} reviews")
            print("   Language distribution:")
            for lang, count in lang_counts.items():
                print(f"   - {LANGUAGE_CONFIG['language_names'].get(lang, lang).title()}: {count}")
        else:
            print("⚠️ No reviews found or error occurred")
        
        # Be nice to the server
        time.sleep(SCRAPING_CONFIG['sleep_time'])
        print(f"⏱️  Completed in {time.time() - start_time:.1f} seconds")
    
    # Save all reviews
    if all_reviews:
        output_path = f"{SCRAPING_CONFIG['output']['directory']}/{SCRAPING_CONFIG['output']['filename']}"
        save_to_csv(all_reviews, output_path)
        
        # Final summary
        print("\n" + "="*60)
        print("🏁 Scraping Complete!")
        print("="*60)
        print(f"📊 Total Reviews: {len(all_reviews)}")
        print(f"💾 Saved to: {output_path}")
        print("="*60)
    else:
        print("\n❌ No reviews were scraped")

if __name__ == "__main__":
    main()