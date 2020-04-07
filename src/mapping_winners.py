import pickle
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import random
import glob
import os
import imageio

def create_mapping_frames(sorted_time_periods, latitutudes, longitudes, colors, labels, jitter=True):
    plt.rcParams["figure.figsize"] = (14,6)
    plt.rcParams.update({'font.size': 16})

    m = Basemap(projection = 'mill', llcrnrlat = 25, llcrnrlon = -130, urcrnrlat = 50, urcrnrlon = -60, resolution = 'l')

    m.drawcoastlines()
    m.drawstates(color="grey")
    m.drawcountries(linewidth=2)

    filenumber = 1

    for i in range(len(sorted_time_periods)):
        cur_time_period = sorted_time_periods[i]
        latitude = latitutudes[i]
        longitude = longitudes[i]
        if jitter:
            latitude += random.uniform(-0.5, 0.5)
            longitude += random.uniform(-0.5, 0.5)
        x, y = m(longitude, latitude)

        m.plot(x, y, color=colors[i], marker="o", markersize=3.5, label=labels[i] if filenumber == 1 else "_nolegend_")
        
        try:
            if cur_time_period == sorted_time_periods[i+1]:
                pass
            else:
                plt.title(f"GABF Medal Wins (Year: {cur_time_period})")
                plt.legend(loc="lower right")
                plt.savefig(f"images/map_frames/{filenumber:03d}.png")
                filenumber += 1
        # Handle last frame
        except IndexError:
            plt.title(f"GABF Medal Wins (Year: {cur_time_period})")
            plt.legend(loc="lower right")
            # Create 5 copies of last frame
            for i in range(5):
                plt.savefig(f"images/map_frames/{filenumber:03d}.png")
                filenumber += 1
    return

def create_gif(folder_of_pngs, file_path_out, frame_rate=0.5, remove_source_files=False):
    images = []
    img_paths = sorted(glob.glob(os.path.join(folder_of_pngs, "*.png")))
    for img in img_paths:
        images.append(imageio.imread(img))
    imageio.mimsave(file_path_out, images, duration=frame_rate)
    if remove_source_files:
        for img in img_paths:
            os.remove(img)
    return

if __name__ == '__main__':


    df = pd.read_csv('data/cleaned_gabf_winners.csv')

    with open("data/coordinates.pkl", "rb") as f:
        coords_dict = pickle.load(f)

    latitutudes_dict = {}
    longitudes_dict = {}
    for location in coords_dict:
        latitutudes_dict[location] = coords_dict[location]['latitude']
        longitudes_dict[location] = coords_dict[location]['longitude']

    medal_colors = {
        "Gold": "#f5bf42",
        "Silver": "#949494",
        "Bronze": "#c47600",
        "Honorable Mention": "#c4ecff"
    }

    # Map medal colors to RGBA
    df['Plot_Color'] = df['Medal'].map(medal_colors)

    # Create locations key and map from pickle file
    df['Locations'] = df['City'] + ", " + df['State']
    df['Latitude'] = df['Locations'].map(latitutudes_dict)
    df['Longitude'] = df['Locations'].map(longitudes_dict)
    
    # Sort DF by years
    df = df.sort_values(by=['Year'])

    latitudes_lst = df['Latitude'].to_list()
    longitudes_lst = df['Longitude'].to_list()
    colors_lst = df['Plot_Color'].to_list()
    years_lst = df['Year'].to_list()
    labels_lst = df['Medal'].to_list()

    create_mapping_frames(years_lst, latitudes_lst, longitudes_lst, colors_lst, labels_lst, jitter=True)
    create_gif("images/map_frames", "images/map_animation.gif", frame_rate=0.5, remove_source_files=True)