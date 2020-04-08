import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geocode_cities import geocode_cities

def create_line_plot(x_vals, y_vals, x_label, y_label, title, filename):
    # Set plotting styles
    plt.style.use("Solarize_Light2")
    plt.rcParams.update({'font.size': 16})
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(x_vals, y_vals)
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_label, fontsize=16)
    ax.set_title(title, fontsize=18)
    plt.savefig(f'images/{filename}')
    plt.close('all')
    return fig

def create_bar_chart_medals(df, groupby_col, n, cluster_medals=True, proportional=False):
    df_state_winners = df.copy()
    # Drop honorable mentions
    df_state_winners = df_state_winners[df_state_winners["Medal"] != "Honorable Mention"]

    # Coallate totals of all medals
    df_total_medals = df_state_winners.groupby(groupby_col).count().reset_index()[[groupby_col, "Medal"]]
    df_total_medals = df_total_medals.sort_values(by=['Medal'], ascending=False)
    df_total_medals = df_total_medals.rename(columns={"Medal": "total_medals"})

    df_golds = df_state_winners[df_state_winners["Medal"] == "Gold"]
    df_golds = df_golds[[groupby_col, "Medal"]]
    df_golds = df_golds.groupby(groupby_col).count().reset_index()
    df_golds = df_golds.rename(columns={"Medal": "gold_medals"})

    df_silvers = df_state_winners[df_state_winners["Medal"] == "Silver"]
    df_silvers = df_silvers[[groupby_col, "Medal"]]
    df_silvers = df_silvers.groupby(groupby_col).count().reset_index()
    df_silvers = df_silvers.rename(columns={"Medal": "silver_medals"})

    df_bronze = df_state_winners[df_state_winners["Medal"] == "Bronze"]
    df_bronze = df_bronze[[groupby_col, "Medal"]]
    df_bronze = df_bronze.groupby(groupby_col).count().reset_index()
    df_bronze = df_bronze.rename(columns={"Medal": "bronze_medals"})

    # Merge medal totals to one dataframe
    df_total_medals = df_total_medals.merge(df_golds, on=groupby_col).merge(df_silvers, on=groupby_col).merge(df_bronze, on=groupby_col)
    df_total_medals_top = df_total_medals.head(n)

    if df_total_medals_top[groupby_col].str.len().max() >= 5:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        x_label_rot = 30
        ha = 'right'
        plt.tight_layout(pad=3)
        if df_total_medals_top[groupby_col].str.len().max() >= 20:
            x_label_font_size = 10
            fig.subplots_adjust(bottom=.25)
        else:
            x_label_font_size = 12
            fig.subplots_adjust(bottom=.2)
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        x_label_rot = 0
        ha = 'center'
        x_label_font_size = 14

    plt.xticks(rotation=x_label_rot, fontsize=x_label_font_size, ha=ha)
    ax.set_ylabel("# of Medals Won", fontsize=16)
    ax.set_title(f"Number of Medals by {groupby_col} (Top {n})", fontsize=18)
    ax.set_xlabel(groupby_col, fontsize=16)
    ax.set_xlabel(groupby_col, fontsize=16)
    
    file_suffix = ""
    if cluster_medals:
        x = np.arange(len(df_total_medals_top[groupby_col]))
        width = 0.2
        ax.bar(x - width, df_total_medals_top['gold_medals'], width, label='Gold', color="#f5bf42", edgecolor="black")
        ax.bar(x, df_total_medals_top['silver_medals'], width, label='Silver', color="#949494", edgecolor="black")
        ax.bar(x + width, df_total_medals_top['bronze_medals'], width, label='Bronze', color="#c47600", edgecolor="black")
        ax.set_xticks(x)
        ax.set_xticklabels(df_total_medals_top[groupby_col])
        ax.legend()
        file_suffix += "_clustered"
    else:
        ax.bar(df_total_medals_top[groupby_col], df_total_medals_top['total_medals'], edgecolor="black")

    plt.savefig(f'images/{groupby_col.lower()}_medals{file_suffix}.png')
    plt.close('all')
    return fig

if __name__ == "__main__":

    df = pd.read_csv('data/cleaned_gabf_winners.csv', index_col=0)

    # Winners over time
    df_year_counts = df.copy()
    df_year_counts['Count'] = ""
    df_year_counts = df_year_counts.groupby("Year").count()[['Count']].reset_index()
    
    create_line_plot(df_year_counts['Year'], df_year_counts['Count'], "Year", "# of Winners", "Number of Winners Over Time", "count_winners_over_time.png")

    # Unique categories over time - Winners are directly related to categories
    df_year_counts_by_cat = df.copy()
    df_year_counts_by_cat = df_year_counts_by_cat[["Year", "Category"]]
    df_year_counts_by_cat = df_year_counts_by_cat.groupby('Year')['Category'].nunique().reset_index()

    create_line_plot(df_year_counts_by_cat['Year'], df_year_counts_by_cat['Category'], "Year", "# of Categories", "Number of Categories Over Time", "count_cats_over_time.png")

    # Unique states over time
    df_year_counts_by_state = df.copy()
    df_year_counts_by_state = df_year_counts_by_state[["Year", "State"]]
    df_year_counts_by_state = df_year_counts_by_state.groupby('Year')['State'].nunique().reset_index()

    create_line_plot(df_year_counts_by_state['Year'], df_year_counts_by_state['State'], "Year", "# of States", "Number of States Over Time", "count_states_over_time.png")

    # States that win the most

    # TODO
    # Add top breweries
    create_bar_chart_medals(df, "State", n=15, cluster_medals=False)
    create_bar_chart_medals(df, "State", n=15, cluster_medals=True)
    

    create_bar_chart_medals(df, "Brewery", n=15, cluster_medals=False)
    create_bar_chart_medals(df, "Brewery", n=15, cluster_medals=True)

    df['City'] = df['City'] + ", " + df['State']
    create_bar_chart_medals(df, "City", n=15, cluster_medals=False)
    create_bar_chart_medals(df, "City", n=15, cluster_medals=True)