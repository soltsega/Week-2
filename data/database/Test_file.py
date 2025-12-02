import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    dbname="bank_reviews",
    user="postgres",
    password="13579.,ad",
    host="localhost"
)

query = """
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY b.bank_name), 1) as percentage
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, r.sentiment_label;
"""

with conn.cursor() as cur:
    cur.execute(query)
    results = cur.fetchall()
    print(tabulate(results, headers=['Bank', 'Sentiment', 'Count', 'Percentage%'], tablefmt='grid'))

conn.close()