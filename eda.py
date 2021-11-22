import numpy as np
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def historical_eda():
    """
    Loads the processed data and provides a historical trend of the homes built 
    in the last century
    """
    zillowHousing = pathlib.Path(r'./data/zillowHousing/clean_data_2016.csv')
    zhData = pd.read_csv(zillowHousing)

    plt.figure(figsize = (20,8))
    ax1 = plt.subplot(1,2,1)
    sns.kdeplot(zhData['yearbuilt'], color = '#004c70', ax=ax1)
    #sns.histplot(data=zhData, x='yearbuilt', stat='count', ax=ax1, kde=True)
    plt.xlim(1900, 2016)
    plt.title('Distribution of Homes built every year', fontsize = 15)