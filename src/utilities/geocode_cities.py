from geopy.geocoders import Bing
from geopy.extra.rate_limiter import RateLimiter
import pickle
import pandas as pd
import os


def geocode_cities(list_of_locations, geolocator):
    coord_dict = {}
    loc_set = set(list_of_locations)
    for loc in loc_set:
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geocode(f"{loc}, USA")
        try:
            coord_dict[loc] = {"latitude": location.latitude, "longitude": location.longitude}
        except Exception as e:
            print(loc)
            print(e)
            pass
    return coord_dict

if __name__ == "__main__":
    geolocator = Bing(api_key=os.getenv('BING_API_KEY'), user_agent="GABF_analysis")
    
    df = pd.read_csv('data/cleaned_gabf_winners.csv', index_col=0)
    df = df[["City", "State"]]
    df["Location"] = df['City'] + ", " + df['State']

    coord_dict = geocode_cities(list(df["Location"]), geolocator)

    f = open("data/coordinates.pkl","wb")

    pickle.dump(coord_dict, f)
    f.close()