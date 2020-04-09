import pickle
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import random
import glob
import os
import imageio

def create_mapping_frames(sorted_time_periods, latitutudes, longitudes, colors, labels, jitter=True):
    """
    Create image frames for a mapping animation over time

    Keyword arguments:
    sorted_time_periods -- list/series of years sorted in ascending order
    latitutudes -- list/series of latitudes
    longitudes -- list/series of longitudes
    colors -- list/series of plot colors
    labels -- list of plot labels
    jitter -- if True, add a bit of jitter to the map
    """
    # set figure params
    plt.rcParams["figure.figsize"] = (10,6)
    plt.rcParams.update({'font.size': 16})

    # load/configure USA map
    m = Basemap(projection = 'mill', llcrnrlat = 25, llcrnrlon = -130, urcrnrlat = 50, urcrnrlon = -60, resolution = 'l')
    m.drawcoastlines()
    m.drawstates(color="grey")
    m.drawcountries(linewidth=2)

    # start a counter for file names
    filenumber = 1
    
    os.makedirs("images/map_frames", exist_ok=True)
    
    for i in range(len(sorted_time_periods)):
        cur_time_period = sorted_time_periods[i]
        latitude = latitutudes[i]
        longitude = longitudes[i]
        if jitter:
            latitude += random.uniform(-0.5, 0.5)
            longitude += random.uniform(-0.5, 0.5)
        
        # convert latitude and longitude to map coordinates
        x, y = m(longitude, latitude)

        # If first year, create legend
        if filenumber == 1:
            label = labels[i] 
        else:
            label = "_nolegend_"

        m.plot(x, y, color=colors[i], alpha=0.5, marker="o", markersize=3, label=label)
        
        try:
            # if year did not change, keep plotting on same frame
            if cur_time_period == sorted_time_periods[i+1]:
                pass
            else:
                plt.title(f"Total GABF Medal Wins (as of {cur_time_period})")
                plt.legend(loc="lower right")
                plt.savefig(f"images/map_frames/{filenumber:03d}.png")
                filenumber += 1
        
        # Handle last frame
        except IndexError:
            plt.title(f"Total GABF Medal Wins (as of {cur_time_period})")
            plt.legend(loc="lower right")
            
            # Create 7 copies of last frame
            for i in range(7):
                plt.savefig(f"images/map_frames/{filenumber:03d}.png")
                filenumber += 1
    return

def create_gif(folder_of_pngs, file_path_out, frame_rate=0.5, remove_source_files=False):
    """
    Create gif from a folder of PNG files

    Keyword arguments:
    folder_of_pngs -- path to folder of png images with files named in ascending order (ex. 001.png, 002.png, etc.)
    file_path_out -- path to output the resulting GIF
    frame_rate -- number of seconds to display each frame. Defaults to 0.5
    remove_source_files -- if True, deletes the frames used to create the GIF
    """
    images = []
    img_paths = sorted(glob.glob(os.path.join(folder_of_pngs, "*.png")))
    for img_path in img_paths:
        images.append(imageio.imread(img_path))
    imageio.mimsave(file_path_out, images, duration=frame_rate)
    if remove_source_files:
        for img_path in img_paths:
            os.remove(img_path)
    return

if __name__ == '__main__':
    df_winners = pd.read_csv('data/cleaned_gabf_winners.csv')

    # load in dictionary of locations -> coordinates written in src/utilities/geocode_cities.py
    with open("data/coordinates.pkl", "rb") as f:
        coords_dict = pickle.load(f)

    latitutudes_dict = {}
    longitudes_dict = {}
    for location in coords_dict:
        latitutudes_dict[location] = coords_dict[location]['latitude']
        longitudes_dict[location] = coords_dict[location]['longitude']
    
    # Map medal colors to RGBA
    medal_colors = {
        "Gold": "#f5bf42",
        "Silver": "#949494",
        "Bronze": "#c47600",
        "Honorable Mention": "#c4ecff"
    }

    df_winners['Plot_Color'] = df_winners['Medal'].map(medal_colors)

    # Create locations key and map from pickle file
    df_winners['Locations'] = df_winners['City'] + ", " + df_winners['State']
    df_winners['Latitude'] = df_winners['Locations'].map(latitutudes_dict)
    df_winners['Longitude'] = df_winners['Locations'].map(longitudes_dict)
    
    # Sort DF by years
    df_winners = df_winners.sort_values(by=['Year'])

    # convert everything to lists to feed into function args
    latitudes_lst = df_winners['Latitude'].to_list()
    longitudes_lst = df_winners['Longitude'].to_list()
    colors_lst = df_winners['Plot_Color'].to_list()
    years_lst = df_winners['Year'].to_list()
    labels_lst = df_winners['Medal'].to_list()

    # call our functions
    create_mapping_frames(years_lst, latitudes_lst, longitudes_lst, colors_lst, labels_lst, jitter=True)
    create_gif("images/map_frames", "images/map_animation.gif", frame_rate=0.5, remove_source_files=True)