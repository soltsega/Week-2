import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_wordcloud(texts, bank_name):
    wordcloud = WordCloud(width=800, height=400, 
                        background_color='white').generate(' '.join(texts))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Common Themes - {bank_name}')
    plt.savefig(f'reports/figures/wordcloud_{bank_name}.png')
    plt.close()