import pandas as pd
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords
from string import punctuation
import re

def remove_words(text, word_list):
    text_lst = text.split(" ")
    return " ".join([v.strip() for v in text_lst if v.lower().strip() not in set(word_list)])

def create_word_list(text_list, stopwords):
    clean_words = []
    for text in text_list:
        clean_text = remove_words(text, stopwords)
        [clean_words.append(word.strip().lower()) for word in re.split(r"[\s\/\-]", clean_text)]
    return clean_words

def create_word_cloud(pd_series, title):
    text = " ".join(name for name in pd_series)
    wordcloud = WordCloud().generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)

    filename = title.lower().replace(" ", "_")
    plt.savefig(f"images/word_cloud_{filename}.png")
    return

if __name__ == '__main__':
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english') + stopwords.words('german') + stopwords.words('french'))

    df = pd.read_csv('data/cleaned_gabf_winners.csv')
    df['Clean Beer Name'] = df['Beer Name'].apply(remove_words, args=(stop_words,))

    create_word_cloud(df['Clean Beer Name'], "Beer Names")

    categories = df['Category'].unique()
    clean_category_word_list = create_word_list(categories, stop_words)

    df['Clean Beer Name Without Categories'] = df['Clean Beer Name'].apply(remove_words, args=(clean_category_word_list,))

    brewery_names = df['Brewery'].unique()
    clean_brewery_word_list = create_word_list(brewery_names, stop_words)

    df['Clean Beer Name Without Categories and Breweries'] = df['Clean Beer Name Without Categories'].apply(remove_words, args=(clean_brewery_word_list,))
    create_word_cloud(df['Clean Beer Name Without Categories and Breweries'], "Beer Names without Brewery or Category Keywords")