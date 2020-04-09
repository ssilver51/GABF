import pandas as pd
import numpy as np

def update_df(df, condition_col, condition_val, update_col, update_val):
    df.loc[df[condition_col] == condition_val, update_col] = update_val
    return df

if __name__ == '__main__':
    df_winners = pd.read_csv('data/gabf_winners.csv', index_col=0)

    # They made the switch from 'First Place', 'Second Place', and 'Third Place' to 'Gold', 'Silver', and 'Bronze'; convert
    df_winners["Medal"] = df_winners["Medal"].replace("First Place", "Gold")
    df_winners["Medal"] = df_winners["Medal"].replace("Second Place", "Silver")
    df_winners["Medal"] = df_winners["Medal"].replace("Third Place", "Bronze")

    # Drop one-off awards
    df_winners = df_winners[df_winners["Medal"] != "Small Brewing Company and Small Brewing Company Brewer of the Year"]
    df_winners = df_winners[df_winners["Medal"] != "Small Brewpub and Small Brewpub Brewer of the Year"]

    # Some states were missing, but using the City and Brewery info, I was able to fill that in
    df_winners = update_df(df_winners, "City", "Cincinnati", "State", "OH")
    df_winners = update_df(df_winners, "City", "Kennesaw", "State", "GA")

    # Some states were using lower-case codes (ex. 'Ak' and 'wa' instead of 'AK' and 'WA')
    df_winners['State'] = df_winners['State'].str.upper()
    
    # Some cities are spelled wrong
    df_winners = update_df(df_winners, "City", "Credted Butte", "City", "Crested Butte")
    df_winners = update_df(df_winners, "City", "Northamapton", "City", "Northampton")
    df_winners = update_df(df_winners, "City", "Jantzen Beach/Lloyd Center/Clear Lake", "City", "Clear Lake")
    df_winners = update_df(df_winners, "City", "Floosmoor", "City", "Flossmoor")
    df_winners = update_df(df_winners, "City", "College Park - Indianapolis", "City", "Indianapolis")

    # Some one mis-typed state name
    df_winners = update_df(df_winners, "City", "New Ulm", "State", "MN")

    # Some states have location data alll grouped into the 'City' column
    new_states = df_winners[df_winners['City'].str.contains(r"\(.+\)") == True]['City'].str.extract(r"\(.+,.*([A-Z]{2})\)").rename(columns={0: "State"})
    new_cities = df_winners[df_winners['City'].str.contains(r"\(.+\)") == True]['City'].str.extract(r"\((.+),.+\)").rename(columns={0: "City"})
    df_winners.update(new_cities)
    df_winners.update(new_states)

    df_winners.to_csv("data/cleaned_gabf_winners.csv")