# Bank Review Analysis System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![CI/CD](https://github.com/yourusername/Week-2/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/Week-2/actions)

A comprehensive data analysis pipeline for processing and analyzing Google Play Store reviews of Ethiopian banking applications. This project is part of the 10 Academy Week 2 Challenge.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [📊 Features](#-features)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [📁 Project Structure](#-project-structure)
- [🔧 Usage](#-usage)
  - [Data Preprocessing](#data-preprocessing)
  - [Sentiment Analysis](#sentiment-analysis)
  - [Thematic Analysis](#thematic-analysis)
  - [Database Integration](#database-integration)
- [🧪 Testing](#-testing)
- [🤖 CI/CD Pipeline](#-cicd-pipeline)
- [📈 Analysis Methodology](#-analysis-methodology)
  - [Sentiment Analysis](#sentiment-analysis-1)
  - [Thematic Analysis](#thematic-analysis-1)
- [📄 Reports and Visualizations](#-reports-and-visualizations)
- [📝 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

## 🌟 Project Overview

This project focuses on analyzing customer satisfaction with mobile banking apps from three major Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The analysis includes:
- Sentiment analysis of user reviews
- Thematic analysis to identify common issues and praises
- Comparative analysis between banks
- Generation of actionable insights for app improvement

## 📊 Features

- **Data Collection**: Automated scraping of Google Play Store reviews
- **Data Preprocessing**: Cleaning and normalization of review text
- **Sentiment Analysis**: Using TextBlob and VADER for sentiment scoring
- **Thematic Analysis**: TF-IDF and word clouds for theme extraction
- **Visualization**: Interactive plots and dashboards
- **Database Integration**: PostgreSQL for data persistence
- **CI/CD**: Automated testing and deployment

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Week-2.git
   cd Week-2
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/bank_reviews
   ```

## 📁 Project Structure

```
Week-2/
├── data/                   # Data storage
│   ├── raw/               # Raw scraped data
│   └── processed/         # Cleaned and processed data
├── reports/               # Analysis reports
│   ├── figures/           # Generated visualizations
│   └── final_report.pdf   # Final analysis report
├── src/
│   ├── analysis/          # Analysis modules
│   │   ├── __init__.py
│   │   ├── sentiments_analyser.py
│   │   └── theme_extractor.py
│   ├── preprocessing/     # Data cleaning
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── .github/workflows/     # CI/CD configuration
├── .gitignore
├── README.md
└── requirements.txt
```

## 🔧 Usage

### Data Preprocessing

```python
from src.preprocessing.preprocess import preprocess_reviews

# Process raw reviews
df_processed = preprocess_reviews('data/raw/bank_reviews.csv')
```

### Sentiment Analysis

```python
from src.analysis.sentiments_analyser import analyze_sentiment_textblob

# Analyze sentiment
result = analyze_sentiment_textblob("Great app, works perfectly!")
print(result)
# Output: {'polarity': 0.8, 'subjectivity': 0.75, 'sentiment': 'positive'}
```

### Thematic Analysis

```python
from src.analysis.theme_extractor import generate_wordcloud, extract_key_themes

# Generate word cloud
reviews = ["Great app", "Terrible experience", "Works well"]
generate_wordcloud(reviews, "CBE")

# Extract key themes
themes = extract_key_themes(reviews, n_topics=3)
```

### Database Integration

```python
from src.database.db_handler import DatabaseHandler

# Initialize database handler
db = DatabaseHandler()

# Save processed data
db.save_reviews(df_processed)

# Query data
reviews = db.get_reviews_by_bank("CBE")
```

## 🧪 Testing

Run the test suite with:

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## 🤖 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

1. Code linting with Flake8
2. Unit testing with pytest
3. Code coverage reporting
4. Automated deployment on successful build

## 📈 Analysis Methodology

### Sentiment Analysis

1. **TextBlob**:
   - Polarity: [-1.0, 1.0] where -1 is negative, 1 is positive
   - Subjectivity: [0.0, 1.0] where 0 is objective, 1 is subjective

2. **VADER**:
   - Compound score: [-1, 1] for negative to positive sentiment
   - Thresholds: Positive (>0.05), Neutral (-0.05 to 0.05), Negative (<-0.05)

### Thematic Analysis

1. **TF-IDF Vectorization**:
   - Converts text to numerical features
   - Weights terms by importance

2. **Topic Modeling**:
   - Latent Dirichlet Allocation (LDA)
   - Non-Negative Matrix Factorization (NMF)

## 📄 Reports and Visualizations

The analysis generates several visualizations:

1. **Sentiment Distribution** by bank
2. **Word Clouds** for each bank
3. **Topic Modeling** visualizations
4. **Time Series Analysis** of sentiment trends

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 10 Academy for the challenge
- Google Play Store for review data
- Open-source community for libraries and tools
- Instructors and mentors at 10 Academy
```

