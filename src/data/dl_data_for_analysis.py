
import kaggle
import os

if __name__ == '__main__':
    # You will need a kaggle API token, see kaggle-api documentation https://github.com/Kaggle/kaggle-api#api-credentials
    if not os.path.exists('data/beer_reviews.csv'):
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('rdoume/beerreviews', path='data', unzip=True)