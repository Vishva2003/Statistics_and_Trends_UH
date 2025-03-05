"""
This is the template file for the statistics and trends assignment.
You will be expected to complete all the sections and
make this a fully working, documented file.
You should NOT change any function, file or variable names,
if they are given to you here.
Make use of the functions presented in the lectures
and ensure your code is PEP-8 compliant, including docstrings.
"""
from corner import corner
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as ss
import seaborn as sns


def plot_relational_plot(df):
    """
    The function `plot_relational_plot` creates a scatter plot comparing the opening and closing prices
    from a DataFrame and saves the plot as a 'relational_plot.png' image.
    """
    
    fig, ax = plt.subplots(figsize=(7,7))
    ax.grid(color = 'gray' , zorder = -3)
    ax.scatter(df['Open'], df['Close'] , zorder = 5, color='r')
    ax.set_xlabel('Opening Price', fontsize = 14)
    ax.set_ylabel('Closing Price', fontsize = 14)
    ax.set_title('Open vs Close',fontsize = 16)
    plt.savefig('relational_plot.png')
    
    return



def plot_categorical_plot(df):
    """
    The function `plot_categorical_plot` generates a bar plot showing the average trading volume by
    month from a given DataFrame and saves the plot as a 'categorical_plot.png' image.
    """
    
    avg_mon = df.groupby('Month')['Volume'].mean()
    fig, ax = plt.subplots(figsize=(7,7))
    plt.grid(color = 'gray' , zorder = -3 , linestyle = '--')
    sns.barplot(x = avg_mon.index , y=avg_mon.values, color='b')
    ax.set_xlabel('Months', fontsize = 14)
    ax.set_ylabel('Avg Trading Volume', fontsize = 14)
    ax.set_title('Avg Trading Volume by Months', fontsize=16)
    plt.xticks(range(0, 12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],color = 'k')
    plt.savefig('categorical_plot.png')
    
    return


def plot_statistical_plot(df):
    """
    The function `plot_statistical_plot` generates a heatmap of the correlation matrix for numerical
    columns in a DataFrame and saves the plot as 'statistical_plot.png'.
    """
    
    fig, ax = plt.subplots(figsize=(7,7))
    df_numeric = df.select_dtypes(include=["number"])
    sns.heatmap(df_numeric.corr(), annot=True , linewidths=0.2, cmap='crest')
    ax.set_title("HeatMap of BitCoin Price" , fontsize = 16)
    plt.savefig('statistical_plot.png')
    
    return


def statistical_analysis(df, col: str):
    """
    The function `statistical_analysis` calculates the mean, standard deviation, skewness, and excess
    kurtosis of a specified column in a DataFrame.
    """
    
    mean = df[col].mean()
    stddev = df[col].std()
    skew = ss.skew(df[col].dropna())
    excess_kurtosis = ss.kurtosis(df[col].dropna())
    return mean, stddev, skew, excess_kurtosis


def preprocessing(df):
    """
    The function preprocesses the input DataFrame by dropping missing values and then displays data
    summary statistics, sample data, and correlation matrix before returning the processed DataFrame.
    """
    
    # You should preprocess your data in this function and
    # make use of quick features such as 'describe', 'head/tail' and 'corr'.
    
    df.dropna(inplace=True)
    print("Data Summary:\n", df.describe())
    print("\nSample Data:\n", df.head(10))
    print("\nCorrelation Matrix:\n", df.corr())
    
    return df


def writing(moments, col):
    """
    The function `writing` calculates and prints descriptive statistics for a given attribute, including
    mean, standard deviation, skewness, and excess kurtosis, and determines whether the data is skewed
    and the type of kurtosis.
    """
    
    mean, stddev, skew, excess_kurtosis = moments
    print(f'\nFor the attribute {col}:')
    print(f'Mean = {mean:.2f}, 'f'Standard Deviation = {stddev:.2f}, 'f'Skewness = {skew:.2f}, and 'f'Excess Kurtosis = {excess_kurtosis:.2f}.')
    
    # Delete the following options as appropriate for your data.
    # Not skewed and mesokurtic can be defined with asymmetries <-2 or >2.
    
    skewness_type = "not skewed" if abs(skew) < 0.5 else "right-skewed" if skew > 0 else "left-skewed"
    kurtosis_type = "mesokurtic" if -0.5 <= excess_kurtosis <= 0.5 else "leptokurtic" if excess_kurtosis > 0.5 else "platykurtic"
    
    print(f'The data was {skewness_type} and {kurtosis_type}.')
    
    return


def main():
    """
    The main function reads a CSV file, preprocesses the data, generates and plots various types of
    plots, performs statistical analysis on a specific column, and writes the results to a file.
    :return: The `main()` function is returning nothing explicitly. It is a void function that performs
    a series of data processing and visualization tasks but does not return any specific value.
    """
    
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month
    df_num = df.select_dtypes(include=['number'])
    
    df = preprocessing(df_num)
    col = 'Open'
    plot_relational_plot(df)
    plot_statistical_plot(df)
    plot_categorical_plot(df)
    moments = statistical_analysis(df, col)
    writing(moments, col)
    return

if __name__ == '__main__':
    main()
