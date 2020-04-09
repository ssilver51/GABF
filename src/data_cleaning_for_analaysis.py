import pandas as pd
import re
from fuzzywuzzy import fuzz
import pickle
import os
import kaggle

def clean_text(text):
    # text = re.sub(r"\s+", "_", text.strip()).lower()
    text = re.sub(r"[!\"#\$%&'\(\)\*\+,-\./:;<=>\?@\[\\\]\^`{\|}~_\s]", "", text).lower().strip()
    return text

def fuzzymatch(text, lst, thresh):
    ratio = 0
    match = ""
    for item in lst:
        new_ratio = fuzz.ratio(text.lower(), item.lower())
        if new_ratio > ratio:
            ratio = new_ratio
            match = item
    if ratio >= thresh:
        return match
    else:
        return text

def save_fuzzy_match_dict(lst1, lst2, thresh, pickle_file_path, overwrite=False):
    if not os.path.exists(pickle_file_path) | overwrite == True:
        fuzzy_dict = {}
        for item in l1:
            fuzzy_dict[item] = fuzzymatch(item, l2, thresh)

        f = open(pickle_file_path, "wb")
        pickle.dump(fuzzy_dict, f)
        f.close()
    return

if __name__ == '__main__':

    # You will need a kaggle API token, see kaggle-api documentation https://github.com/Kaggle/kaggle-api#api-credentials
    if not os.path.exists('data/beer_reviews.csv'):
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('rdoume/beerreviews', path='data', unzip=True)

    df_reviews = pd.read_csv('data/beer_reviews.csv')
    df_reviews = df_reviews.dropna(subset=['beer_name', 'brewery_name'])
    df_reviews = df_reviews.drop(columns=['review_time', 'review_profilename', 'beer_style', 'beer_abv'])

    df_gabf = pd.read_csv('data/gabf_winners.csv')
    df_gabf = df_gabf.drop(columns=['City', 'State', 'Category', 'Year'])

    df_reviews['clean_brewery_name'] = df_reviews['brewery_name'].apply(clean_text)
    df_reviews['clean_beer_name'] = df_reviews['beer_name'].apply(clean_text)
    df_gabf['clean_brewery_name'] = df_gabf['Brewery'].apply(clean_text)
    df_gabf['clean_beer_name'] = df_gabf['Beer Name'].apply(clean_text)

    # Create dicts of fuzzy matches - O(n^2) worst case
    l1 = df_reviews['clean_beer_name'].unique()
    l2 = df_gabf['clean_beer_name'].unique()
    save_fuzzy_match_dict(l1, l2, 90, "data/fuzzy_beer_name_map.pkl", overwrite=False)

    l1 = df_reviews['clean_brewery_name'].unique()
    l2 = df_gabf['clean_brewery_name'].unique()
    save_fuzzy_match_dict(l1, l2, 90, "data/fuzzy_brewery_name_map.pkl", overwrite=False)

    with open("data/fuzzy_beer_name_map.pkl", "rb") as f:
        beer_name_map = pickle.load(f)
    with open("data/fuzzy_brewery_name_map.pkl", "rb") as f:
        brewery_name_map = pickle.load(f)

    df_reviews['clean_beer_name'] = df_reviews['clean_beer_name'].map(beer_name_map)
    df_reviews['clean_brewery_name'] = df_reviews['clean_brewery_name'].map(brewery_name_map)

    df_merged = pd.merge(df_reviews, df_gabf, on=['clean_brewery_name', 'clean_beer_name'], how='left')

    df_reviews_gabf_winners = df_merged[df_merged['Medal'].notnull()].drop(columns=df_gabf.columns)
    df_reviews_not_winners = df_merged[df_merged['Medal'].isnull()].drop(columns=df_gabf.columns)

    # Save cleaned data files and remove original
    df_reviews_gabf_winners.to_csv("data/reviews_gabf.csv")
    df_reviews_not_winners.to_csv("data/reviews_non_gabf.csv")
    os.remove("data/beer_reviews.csv")