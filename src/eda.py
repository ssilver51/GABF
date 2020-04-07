import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geocode_cities import geocode_cities

def create_line_plot(x_vals, y_vals, x_label, y_label, title, filename):
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(x_vals, y_vals)
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_label, fontsize=16)
    ax.set_title(title, fontsize=18)

    plt.savefig(f'images/{filename}')
    plt.close('all')
    return fig

if __name__ == "__main__":
    # Set plotting styles
    plt.style.use("Solarize_Light2")
    plt.rcParams.update({'font.size': 16})

    df = pd.read_csv('data/cleaned_gabf_winners.csv', index_col=0)

    # Winners over time
    df_year_counts = df.copy()
    df_year_counts['Count'] = ""
    df_year_counts = df_year_counts.groupby("Year").count()[['Count']].reset_index()
    
    create_line_plot(df_year_counts['Year'], df_year_counts['Count'], "Year", "# of Winners", "# of Winners Over Time", "count_winners_over_time.png")

    # Unique categories over time - Winners are directly related to categories
    df_year_counts_by_cat = df.copy()
    df_year_counts_by_cat = df_year_counts_by_cat[["Year", "Category"]]
    df_year_counts_by_cat = df_year_counts_by_cat.groupby('Year')['Category'].nunique().reset_index()

    create_line_plot(df_year_counts_by_cat['Year'], df_year_counts_by_cat['Category'], "Year", "# of Categories", "# of Categories Over Time", "count_cats_over_time.png")

    # Unique states over time
    df_year_counts_by_state = df.copy()
    df_year_counts_by_state = df_year_counts_by_state[["Year", "State"]]
    df_year_counts_by_state = df_year_counts_by_state.groupby('Year')['State'].nunique().reset_index()

    create_line_plot(df_year_counts_by_state['Year'], df_year_counts_by_state['State'], "Year", "# of States", "# of States Over Time", "count_states_over_time.png")

    # States that win the most

    df_state_winners = df.copy()
    # Drop honorable mentions
    df_state_winners = df_state_winners[df_state_winners["Medal"] != "Honorable Mention"]

    df_state_medals = df_state_winners.groupby('State').count().reset_index()[["State", "Medal"]]
    df_state_medals = df_state_medals.sort_values(by=['Medal'], ascending=False)
    df_state_medals = df_state_medals.rename(columns={"Medal": "total_medals"})

    df_state_golds = df_state_winners[df_state_winners["Medal"] == "Gold"]
    df_state_golds = df_state_golds[["State", "Medal"]]
    df_state_golds = df_state_golds.groupby('State').count().reset_index()
    df_state_golds = df_state_golds.rename(columns={"Medal": "gold_medals"})

    df_state_silvers = df_state_winners[df_state_winners["Medal"] == "Silver"]
    df_state_silvers = df_state_silvers[["State", "Medal"]]
    df_state_silvers = df_state_silvers.groupby('State').count().reset_index()
    df_state_silvers = df_state_silvers.rename(columns={"Medal": "silver_medals"})

    df_state_bronze = df_state_winners[df_state_winners["Medal"] == "Bronze"]
    df_state_bronze = df_state_bronze[["State", "Medal"]]
    df_state_bronze = df_state_bronze.groupby('State').count().reset_index()
    df_state_bronze = df_state_bronze.rename(columns={"Medal": "bronze_medals"})

    df_state_medals = df_state_medals.merge(df_state_golds, on='State').merge(df_state_silvers, on='State').merge(df_state_bronze, on='State')
    df_state_medals_top_15 = df_state_medals.head(15)

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.bar(df_state_medals_top_15['State'], df_state_medals_top_15['total_medals'])
    ax.set_xlabel("State", fontsize=16)
    ax.set_ylabel("# of Medals Won", fontsize=16)
    ax.set_title("# of Medals by State (Top 15)", fontsize=18)
    plt.savefig('images/state_medals.png')
    plt.close('all')

    # Grouped bar chart
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    x = np.arange(len(df_state_medals_top_15['State']))
    width = 0.25

    ax.bar(x - width, df_state_medals_top_15['gold_medals'], width, label='Gold', color="#f5bf42", edgecolor="black")
    ax.bar(x, df_state_medals_top_15['silver_medals'], width, label='Silver', color="#949494", edgecolor="black")
    ax.bar(x + width, df_state_medals_top_15['bronze_medals'], width, label='Bronze', color="#c47600", edgecolor="black")

    ax.set_xlabel("State", fontsize=16)
    ax.set_ylabel("# of Medals Won", fontsize=16)
    ax.set_title("# of Medals by State (Top 15)", fontsize=18)
    ax.set_xticks(x)
    ax.set_xticklabels(df_state_medals_top_15['State'])
    ax.legend()
    plt.savefig('images/state_medals_broken.png')
    plt.close('all')
