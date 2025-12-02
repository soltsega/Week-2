import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

# create a database 
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

def create_database():
    # Load environment variables
    load_dotenv()
    
    # Get database connection parameters
    db_params = {
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '13579.,ad'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': 'postgres'  # Connect to default 'postgres' database first
    }
    
    # Connect to the default 'postgres' database
    conn = psycopg2.connect(**db_params)
    conn.autocommit = True  # Required for creating databases
    
    try:
        with conn.cursor() as cursor:
            # Check if database already exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'bank_reviews'")
            exists = cursor.fetchone()
            
            if not exists:
                # Create the database
                print("Creating database 'bank_reviews'...")
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier('bank_reviews'))
                )
                print("✅ Database 'bank_reviews' created successfully!")
            else:
                print("ℹ️ Database 'bank_reviews' already exists.")
                
    except Exception as e:
        print(f"❌ Error creating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()


# Load environment variables
load_dotenv()

class BankReviewLoader:
    def __init__(self):
        try:
            # Database connection parameters
            self.db_user = os.getenv('DB_USER', 'postgres')
            self.db_password = os.getenv('DB_PASSWORD', '13579.,ad')
            self.db_host = os.getenv('DB_HOST', 'localhost')
            self.db_port = os.getenv('DB_PORT', '5432')
            self.db_name = os.getenv('DB_NAME', 'bank_reviews')
            
            # Use the current directory for CSV files
            self.data_dir = Path(r"C:/Users/My Device/Desktop/Week-2/data/processed")
            
            # Create database engine
            self.engine = create_engine(
                f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            )
            
            # Bank files mapping
            self.bank_files = {
                'Commercial Bank of Ethiopia': 'cleaned_bank_reviews_cbe.csv',
                'Bank of Abyssinia': 'cleaned_bank_reviews_boa.csv',
                'Dashen Bank': 'cleaned_bank_reviews_dashen.csv'
            }
            
            print("✅ Database connection initialized")
            
        except Exception as e:
            print(f"❌ Error initializing database connection: {str(e)}")
            raise

    def test_connection(self):
        """Test the database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connection test successful")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                DROP TABLE IF EXISTS reviews;
                DROP TABLE IF EXISTS banks;
                
                CREATE TABLE banks (
                    bank_id SERIAL PRIMARY KEY,
                    bank_name VARCHAR(100) UNIQUE,
                    app_name VARCHAR(100)
                );

                CREATE TABLE reviews (
                    review_id SERIAL PRIMARY KEY,
                    bank_id INTEGER REFERENCES banks(bank_id),
                    review_text TEXT,
                    rating INTEGER,
                    review_date DATE,
                    sentiment_label VARCHAR(20),
                    sentiment_score FLOAT,
                    source VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """))
                conn.commit()
                print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating tables: {str(e)}")
            raise

    def load_bank_data(self, bank_name, file_path):
        """Load data for a single bank"""
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            print(f"📊 Read {len(df)} rows from {file_path}")
            
            with self.engine.begin() as conn:  # Use begin() for transaction management
                # Insert bank if not exists
                result = conn.execute(
                    text("""
                    INSERT INTO banks (bank_name, app_name)
                    VALUES (:bank_name, :app_name)
                    ON CONFLICT (bank_name) 
                    DO UPDATE SET app_name = EXCLUDED.app_name
                    RETURNING bank_id
                    """),
                    {"bank_name": bank_name, "app_name": f"{bank_name} Mobile"}
                )
                bank_id = result.scalar()
                
                # Prepare reviews data
                reviews_df = df[['review', 'rating', 'date', 'sentiment_label', 'sentiment_score', 'source']].copy()
                reviews_df['bank_id'] = bank_id
                reviews_df = reviews_df.rename(columns={
                    'review': 'review_text',
                    'date': 'review_date'
                })
                
                # Insert reviews
                reviews_df.to_sql(
                    'reviews', 
                    self.engine, 
                    if_exists='append', 
                    index=False, 
                    method='multi', 
                    chunksize=1000
                )
                print(f"✅ Loaded {len(reviews_df)} reviews for {bank_name}")
                return True
                
        except Exception as e:
            print(f"❌ Error loading data for {bank_name}: {str(e)}")
            return False

    def verify_data(self):
        """Verify that data was loaded correctly"""
        try:
            with self.engine.connect() as conn:
                # Count reviews per bank
                result = conn.execute(text("""
                    SELECT b.bank_name, COUNT(*) as review_count
                    FROM reviews r
                    JOIN banks b ON r.bank_id = b.bank_id
                    GROUP BY b.bank_name
                    ORDER BY review_count DESC;
                """))
                
                print("\n📊 Review Counts by Bank:")
                print("=" * 30)
                for row in result:
                    print(f"🏦 {row.bank_name}: {row.review_count} reviews")
                
                # Check for missing data
                result = conn.execute(text("""
                    SELECT 
                        COUNT(*) as total_reviews,
                        COUNT(CASE WHEN review_text IS NULL OR review_text = '' THEN 1 END) as missing_reviews,
                        COUNT(CASE WHEN rating IS NULL THEN 1 END) as missing_ratings
                    FROM reviews;
                """))
                stats = result.fetchone()
                
                print("\n🔍 Data Quality Check:")
                print("=" * 30)
                print(f"📝 Total reviews: {stats.total_reviews}")
                if stats.total_reviews > 0:
                    print(f"❌ Missing review text: {stats.missing_reviews} ({(stats.missing_reviews/stats.total_reviews)*100:.2f}%)")
                    print(f"❌ Missing ratings: {stats.missing_ratings} ({(stats.missing_ratings/stats.total_reviews)*100:.2f}%)")
                
        except Exception as e:
            print(f"❌ Error verifying data: {str(e)}")
            raise

    def run(self):
        """Main method to run the ETL process"""
        print("\n" + "="*50)
        print("🏦 Starting Bank Reviews ETL Process")
        print("="*50)
        
        try:
            # Test connection first
            if not self.test_connection():
                return False
            
            # Create tables (drops existing ones)
            self.create_tables()
            
            # Load data for each bank
            success_count = 0
            for bank_name, filename in self.bank_files.items():
                file_path = self.data_dir / filename
                if file_path.exists():
                    print(f"\n🔍 Processing {bank_name} from {file_path}")
                    if self.load_bank_data(bank_name, file_path):
                        success_count += 1
                else:
                    print(f"\n❌ Error: File not found - {file_path}")
            
            # Verify data if any bank was loaded successfully
            if success_count > 0:
                print("\n" + "="*50)
                print("🔍 Verifying loaded data...")
                print("="*50)
                self.verify_data()
            
            print("\n" + "="*50)
            print("✅ ETL process completed successfully!")
            print("="*50)
            return True
            
        except Exception as e:
            print(f"\n❌ ETL process failed: {str(e)}")
            return False

if __name__ == "__main__":
    try:
        loader = BankReviewLoader()
        if not loader.run():
            exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        exit(1)