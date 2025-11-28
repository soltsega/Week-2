# App configurations
BANK_APPS = {
    'cbe': {
        'id': 'com.combanketh.mobilebanking',
        'name': 'CBE',
        'supported_languages': ['en', 'am']  # English and Amharic
    },
    'boa': {
        'id': 'com.boa.boaMobileBanking',
        'name': 'BOA',
        'supported_languages': ['en', 'am']
    },
    'dashen': {
        'id': 'com.dashen.dashensuperapp',
        'name': 'DASHEN',
        'supported_languages': ['en', 'am']
    }
}

# Language configuration
LANGUAGE_CONFIG = {
    'default_language': 'en',
    'target_language': 'en',  # Language to translate to
    'supported_languages': ['en', 'am'],
    'language_names': {
        'en': 'English',
        'am': 'Amharic'
    }
}

# Translation configuration
TRANSLATION_CONFIG = {
    'enabled': True,
    'provider': 'google',  # 'google', 'mymemory', or 'libre'
    'timeout': 5,  # seconds
    'retries': 3,
    'batch_size': 10  # Number of texts to translate in a single batch
}

# Scraping configuration
SCRAPING_CONFIG = {
    'reviews_per_language': 200,  # Per language
    'country': 'et',              # Ethiopia
    'sleep_time': 2,              # Seconds between requests
    'sort_by': 'most_relevant',   # most_relevant, newest, rating
    'output': {
        'directory': 'data',
        'filename': 'bank_reviews.csv',
        'encoding': 'utf-8-sig'   # For Excel compatibility
    }
}

# Emoji processing
EMOJI_CONFIG = {
    'extract_emojis': True,
    'emoji_columns': {
        'emojis': 'emojis',
        'count': 'emoji_count',
        'descriptions': 'emoji_descriptions'
    }
}

# Data validation
VALIDATION = {
    'min_review_length': 3,
    'allowed_ratings': [1, 2, 3, 4, 5]
}