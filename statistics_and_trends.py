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
    
    fig, ax = plt.subplots(figsize=(7,7))
    ax.grid(color = 'gray' , zorder = -3)
    ax.scatter(df['Open'], df['Close'] , zorder = 5, color='r')
    ax.set_xlabel('Opening Price', fontsize = 14)
    ax.set_ylabel('Closing Price', fontsize = 14)
    ax.set_title('Open vs Close',fontsize = 16)
    plt.savefig('relational_plot.png')
    
    return



def plot_categorical_plot(df):
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
    
    fig, ax = plt.subplots(figsize=(7,7))
    df_numeric = df.select_dtypes(include=["number"])
    sns.heatmap(df_numeric.corr(), annot=True , linewidths=0.2, cmap='crest')
    ax.set_title("HeatMap of BitCoin Price" , fontsize = 16)
    plt.savefig('statistical_plot.png')
    
    return


def statistical_analysis(df, col: str):
    
    mean = df[col].mean()
    stddev = df[col].std()
    skew = ss.skew(df[col].dropna())
    excess_kurtosis = ss.kurtosis(df[col].dropna())
    return mean, stddev, skew, excess_kurtosis


def preprocessing(df):
    # You should preprocess your data in this function and
    # make use of quick features such as 'describe', 'head/tail' and 'corr'.
    df.dropna(inplace=True)
    print("Data Summary:\n", df.describe())
    print("\nSample Data:\n", df.head(10))
    print("\nCorrelation Matrix:\n", df.corr())
    return df


def writing(moments, col):
    
    mean, stddev, skew, excess_kurtosis = moments
    print(f'\nFor the attribute {col}:')
    print(f'Mean = {mean:.2f}, 'f' Standard Deviation = {stddev:.2f}, 'f' Skewness = {skew:.2f}, and 'f'Excess Kurtosis = {excess_kurtosis:.2f}.')
    # Delete the following options as appropriate for your data.
    # Not skewed and mesokurtic can be defined with asymmetries <-2 or >2.
    
    skewness_type = "not skewed" if abs(skew) < 0.5 else "right-skewed" if skew > 0 else "left-skewed"
    kurtosis_type = "mesokurtic" if -0.5 <= excess_kurtosis <= 0.5 else "leptokurtic" if excess_kurtosis > 0.5 else "platykurtic"
    
    
    print(f'The data was {skewness_type} and {kurtosis_type}.')
    return


def main():
    
    df = pd.read_csv('data.csv')
    
    df["Month"] = df["Date"].dt.month
    df_num = df.select_dtypes(include=["number"])
    df = preprocessing(df_num)
    col = 'Open'
    plot_relational_plot(df_num)
    plot_statistical_plot(df_num)
    plot_categorical_plot(df_num)
    moments = statistical_analysis(df_num, col)
    writing(moments, col)
    return

if __name__ == '__main__':
    main()
