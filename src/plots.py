import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Union, List

def plot_correlation_heatmap(df: pd.DataFrame):
    "Plots the correlation Matrix"
    corr_matrix = df.corr()

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create a heatmap of the correlation matrix
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)

    # Set the title
    ax.set_title('Correlation Heatmap')

    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()


def plot_ts(data: pd.DataFrame, product: str, site: str,cols: Union[str, List[str]], legend=None):
    """
    Plots a time series of the data. A time series corresponds to the evolution of stocks for a 
    given product code and site code.
    """
    sns.set()
    plt.rcParams["figure.figsize"] = (35,15)

    data_prod_site = data.loc[(data.loc[:,'site_code']==site) & (data.loc[:,'product_code']==product) ,]
    data_prod_site.index = data_prod_site['date']
    sorted_idx = data_prod_site.index.sort_values()
    data_prod_site = data_prod_site.loc[sorted_idx,]

    if legend:
        legend=cols

    if type(cols)==str:
        plt.plot(data_prod_site.index, data_prod_site[cols], label=legend)
    else:
        for col in cols:
            plt.plot(data_prod_site.index, data_prod_site[col], label=col)
    plt.title(f'Time series stocks for product {product} and site code {site}')
    plt.legend()


def plot_ts2(data: pd.DataFrame, product: str, site: str, cols: Union[str, List[str]], legend=None):
    """
    Plots a time series of the data. A time series corresponds to the evolution of stocks for a 
    given product code and site code.
    """
    sns.set(style='whitegrid')
    plt.rcParams["figure.figsize"] = (12, 6)  # Set the figure size

    data_prod_site = data.loc[(data.loc[:,'site_code']==site) & (data.loc[:,'product_code']==product) ,]
    #data_prod_site['date'] = pd.to_datetime(data_prod_site['date'])  # Convert 'date' column to datetime
    data_prod_site = data_prod_site.sort_values('date')  # Sort data by date

    if legend:
        legend = cols

    if isinstance(cols, str):
        plt.plot(data_prod_site['date'], data_prod_site[cols], label=legend)
    else:
        for col in cols:
            plt.plot(data_prod_site['date'], data_prod_site[col], label=col)

    plt.title(f'Time series stocks for product {product} and site code {site}', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Stocks', fontsize=12)
    plt.legend(fontsize=10)

    sns.despine()  # Remove spines from the plot

    plt.show()
