import pandas as pd
import numpy as np

def update_df(df, condition_col, condition_val, update_col, update_val):
    df.loc[df[condition_col] == condition_val, update_col] = update_val
    return df

if __name__ == '__main__':
    df = pd.read_csv('data/gabf_winners.csv', index_col=0)

    # They made the switch from 'First Place', 'Second Place', and 'Third Place' to 'Gold', 'Silver', and 'Bronze'
    df["Medal"] = df["Medal"].replace("First Place", "Gold")
    df["Medal"] = df["Medal"].replace("Second Place", "Silver")
    df["Medal"] = df["Medal"].replace("Third Place", "Bronze")

    # Drop one-off awards
    df = df[df["Medal"] != "Small Brewing Company and Small Brewing Company Brewer of the Year"]
    df = df[df["Medal"] != "Small Brewpub and Small Brewpub Brewer of the Year"]

    # Some states were missing, but using the City and Brewery info, I was able to fill that in
    df = update_df(df, "City", "Cincinnati", "State", "OH")
    df = update_df(df, "City", "Kennesaw", "State", "GA")

    # Some states were using lower-case codes (ex. 'Ak' and 'wa' instead of 'AK' and 'WA')
    df['State'] = df['State'].str.upper()
    
    # Some cities are spelled wrong
    df = update_df(df, "City", "Credted Butte", "City", "Crested Butte")
    df = update_df(df, "City", "Northamapton", "City", "Northampton")
    df = update_df(df, "City", "Jantzen Beach/Lloyd Center/Clear Lake", "City", "Clear Lake")
    df = update_df(df, "City", "Floosmoor", "City", "Flossmoor")
    df = update_df(df, "City", "College Park - Indianapolis", "City", "Indianapolis")

    # Some one mis-typed state name
    df = update_df(df, "City", "New Ulm", "State", "MN")


    # Some states have location data alll grouped into the 'City' column
    new_states = df[df['City'].str.contains(r"\(.+\)") == True]['City'].str.extract(r"\(.+,.*([A-Z]{2})\)").rename(columns={0: "State"})
    new_cities = df[df['City'].str.contains(r"\(.+\)") == True]['City'].str.extract(r"\((.+),.+\)").rename(columns={0: "City"})
    df.update(new_cities)
    df.update(new_states)

    df.to_csv("data/cleaned_gabf_winners.csv")