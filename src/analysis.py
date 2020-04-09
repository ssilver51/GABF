import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np



def std_err(sample):
    """
    calculate standard error from a sample
    """
    return (sample.std())/(np.sqrt(len(sample)))

def sample_statistics(sample):
    """
    calculate sample statistics
    """
    stats = {
        "mean": sample.mean(),
        "sample size": len(sample),
        "standard deviation": sample.std(),
        "standard error": std_err(sample)
    }
    return stats

def plot_norm_distributions(sample1, sample2, color1, color2, title, x_label, filepath, standard_deviations=4):
    """
    Plot two distributions on the same plot

    Keyword arguments:
    sample1 -- list or series of data
    sample2 -- list or series of data
    color1 -- color of distribution line for sample1
    color2 -- color of distribution line for sample2
    title -- plot title
    x_label -- x axis label
    filepath -- output image path
    standard_deviations -- number of standard deviations from the mean to plot (default: 4)
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    dist1 = stats.norm(loc=sample1.mean(), scale=std_err(sample1))
    dist2 = stats.norm(loc=sample2.mean(), scale=std_err(sample2))

    x_vals = np.linspace(sample1.mean() - standard_deviations * std_err(sample1), sample1.mean() + standard_deviations * std_err(sample1), 100)
    y_vals = dist1.pdf(x_vals)

    x_vals2 = np.linspace(sample2.mean() - standard_deviations * std_err(sample2), sample2.mean() + standard_deviations * std_err(sample2), 100)
    y_vals2 = dist2.pdf(x_vals2)

    ax.plot(x_vals, y_vals, label='Non-GABF Winners', color=color1, alpha=0.5)
    ax.plot(x_vals2, y_vals2, label='GABF Winners', color=color2, alpha=0.5)

    ax.legend()
    ax.set_xlabel(x_label)
    plt.title(title)
    plt.savefig(filepath)
    return fig

def plot_p_value(sample1, sample2, color, title, x_label, filepath):
    """
    Plot a distribution with sample mean, display p-value and z-score
    note: sample1.mean() < sample2.mean()

    Keyword arguments:
    sample1 -- list or series of data
    sample2 -- list or series of data
    color -- color of distribution line
    title -- chart title
    x_label -- x axis label
    filepath -- output image file path
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    sample2_mean = sample2.mean()

    dist1 = stats.norm(loc=sample1.mean(), scale=std_err(sample1))

    z_score = (sample2_mean - sample1.mean())/std_err(sample1)
    p_value = 1 - dist1.cdf(sample2_mean)

    x_vals = np.linspace(sample1.mean() - 4 * std_err(sample1), sample2_mean + 4 * std_err(sample1), 1000)
    y_vals = dist1.pdf(x_vals)

    ax.plot(x_vals, y_vals, label='Non-GABF Winners', color=color, alpha=0.5)

    ax.axvline(x=sample2_mean, linestyle='--', color='red', alpha=0.5, label="GABF Winner Mean Review")
    ax.text(x=(sample2_mean - std_err(sample2) * 0.5), y=0.1*max(y_vals), s=f"z-score ~ {z_score:.2f}\np value ~ {p_value}", horizontalalignment='right', fontsize=12)

    ax.legend()
    ax.set_xlabel(x_label)
    plt.title(title)
    plt.savefig(filepath)
    return fig

if __name__ == '__main__':
    plt.style.use("Solarize_Light2")
    plt.rcParams.update({'font.size': 16})

    # Ho: mean of gabf reviews <= mean of non-gabf reviews
    # Ha: mean of gabf reviews > mean of non-gabf reviews

    alpha = 0.1

    gabf_reviews = pd.read_csv("data/reviews_gabf.csv")
    non_gabf_reviews = pd.read_csv("data/reviews_non_gabf.csv")

    plot_norm_distributions(\
            non_gabf_reviews['review_overall'], gabf_reviews['review_overall'], \
            "blue", "red", \
            "Probability Density Functions - Overall Reviews", \
            "Review Score (1-5)", "images/overall_reviews_dists.png", standard_deviations=5.5
        )
    
    plot_p_value(\
            non_gabf_reviews['review_overall'], gabf_reviews['review_overall'], \
            "blue", "Probability Density Function - Overall Reviews", "Review Score (1-5)", "images/overall_review_p_val.png"
        )
