import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Union, List

def plot_ts(data: pd.DataFrame, product: str, site: str,cols: Union[str, List[str]], legend=None):
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