import pandas as pd
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords
from string import punctuation
import re

def remove_words(text, word_list):
    """
    remove words found in word_list from text
    """
    text_lst = text.split(" ")
    return " ".join([v.strip() for v in text_lst if v.lower().strip() not in set(word_list)])

def create_word_list(text_list, stopwords):
    """
    create wordlist from a list/series of text (excluding stopwords)
    """
    clean_words = []
    for text in text_list:
        clean_text = remove_words(text, stopwords)
        [clean_words.append(word.strip().lower()) for word in re.split(r"[\s\/\-]", clean_text)]
    return clean_words

def create_word_cloud(pd_series, title):
    """
    create a word cloud from a pandas series of text with a given plot title
    """
    text = " ".join(name for name in pd_series)
    wordcloud = WordCloud(mode="RGBA", background_color=None, width=800, height=400).generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    filename = title.lower().replace(" ", "_")
    plt.savefig(f"images/word_cloud_{filename}.png")
    return

if __name__ == '__main__':
    # Download stopwords
    nltk.download('stopwords')

    # beer has lots of stop words
    stop_words = set(stopwords.words('english') + stopwords.words('german') + stopwords.words('french'))

    df_winners = pd.read_csv('data/cleaned_gabf_winners.csv')
    
    # Remove stop words
    df_winners['Clean Beer Name'] = df_winners['Beer Name'].apply(remove_words, args=(stop_words,))

    create_word_cloud(df_winners['Clean Beer Name'], "Beer Names")

    # Remove category keywords
    categories = df_winners['Category'].unique()
    clean_category_word_list = create_word_list(categories, stop_words)

    df_winners['Clean Beer Name Without Categories'] = df_winners['Clean Beer Name'].apply(remove_words, args=(clean_category_word_list,))

    # Remove brewery keywords
    brewery_names = df_winners['Brewery'].unique()
    clean_brewery_word_list = create_word_list(brewery_names, stop_words)

    # Oof, long column names
    df_winners['Clean Beer Name Without Categories and Breweries'] = df_winners['Clean Beer Name Without Categories'].apply(remove_words, args=(clean_brewery_word_list,))
    create_word_cloud(df_winners['Clean Beer Name Without Categories and Breweries'], "Beer Names without Brewery or Category Keywords")