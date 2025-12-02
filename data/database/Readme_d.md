# Bank Reviews Database Schema

## Overview
This document describes the PostgreSQL database schema used to store and analyze bank app reviews from the Google Play Store.

## Database Information
- **Database Name**: `bank_reviews`
- **Host**: `localhost`
- **Port**: `5432`
- **Username**: `postgres` 

## The folder structure in vs code
Week-2/
├── data/
│   ├── database/
│   │   ├── load_to_postgres.py
│   │   ├── adding_sentiment_score&label.py
│   │   ├── .env.example
│   │   └── requirements.txt
├── README.md      <-- Create it here
└── (other files/folders)

## Schema

### 1. `banks` Table
Stores information about each bank's mobile application.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `bank_id` | SERIAL | PRIMARY KEY | Auto-incrementing unique identifier |
| `bank_name` | VARCHAR(100) | NOT NULL | Full name of the bank (e.g., "Commercial Bank of Ethiopia") |
| `app_name` | VARCHAR(100) | NOT NULL | Name of the mobile application |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the record was created |

### 2. `reviews` Table
Stores individual user reviews with sentiment analysis results.

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `review_id` | SERIAL | PRIMARY KEY | Auto-incrementing unique identifier |
| `bank_id` | INTEGER | FOREIGN KEY | References `banks(bank_id)` |
| `review_text` | TEXT | NOT NULL | The full text of the review |
| `rating` | INTEGER | CHECK (rating BETWEEN 1 AND 5) | Star rating from 1 to 5 |
| `review_date` | DATE | NOT NULL | When the review was posted |
| `sentiment_label` | VARCHAR(10) |  | 'positive', 'negative', or 'neutral' |
| `sentiment_score` | FLOAT |  | Sentiment score between -1.0 and 1.0 |
| `source` | VARCHAR(50) | DEFAULT 'Google Play' | Source of the review |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the record was created |

## Setup Instructions

### Prerequisites
- PostgreSQL 12+
- Python 3.8+
- Required Python packages (see [requirements.txt](cci:7://file:///c:/Users/My%20Device/Desktop/Week-2/data/database/requirements.txt:0:0-0:0))

### Database Creation
1. Create the database:
   ```bash
   createdb bank_reviews