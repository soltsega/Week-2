import pandas as pd
from textblob import TextBlob

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob and return label and score"""
    if pd.isna(text) or str(text).strip() == '':
        return 'neutral', 0.0
    
    analysis = TextBlob(str(text))
    score = analysis.sentiment.polarity
    
    if score > 0:
        return 'positive', score
    elif score < 0:
        return 'negative', score
    else:
        return 'neutral', score

def process_bank_reviews(input_file, output_file=None):
    """Process a bank's reviews and add sentiment analysis"""
    if output_file is None:
        output_file = input_file
    
    print(f"Processing {input_file}...")
    
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Add sentiment analysis if columns don't exist
    if 'sentiment_label' not in df.columns or 'sentiment_score' not in df.columns:
        print("  Adding sentiment analysis...")
        # Apply sentiment analysis to each review
        sentiment_results = df['review'].apply(analyze_sentiment)
        df['sentiment_label'] = [result[0] for result in sentiment_results]
        df['sentiment_score'] = [result[1] for result in sentiment_results]
        
        # Save the updated DataFrame
        df.to_csv(output_file, index=False)
        print(f"  ✅ Added sentiment analysis to {output_file}")
    else:
        print("  ✅ Sentiment columns already exist")
    
    return df

# Process all three bank review files
bank_files = [
    'cleaned_bank_reviews_cbe.csv',
    'cleaned_bank_reviews_boa.csv',
    'cleaned_bank_reviews_dashen.csv'
]

# Directory where your CSV files are located
data_dir = r"C:/Users/My Device/Desktop/Week-2/data/processed"

for filename in bank_files:
    input_path = f"{data_dir}/{filename}"
    process_bank_reviews(input_path)

print("\nAll files processed successfully!")