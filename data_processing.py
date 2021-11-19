#Library imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

MISSING_PERCENT_THRESHOLD = 95

def clean_data(fname, plots=False):
    '''
    Read data, find missing values and reduce feature set
    df : data frame
    plots: Draw a bar plot of the % of missing values, if true
    returns: clean dataframe
    '''
    assert isinstance(fname, str) and fname[len(fname)-4:]=='.csv', 'Input filename must be a csv file'
    
    # read in the csv file
    pd.options.display.float_format = '{:,.3f}'.format
    data = pd.read_csv('data/properties_2016.csv')
    data.columns = [column.strip() for column in data.columns]  #clean data colunm names

    #find missing data info
    missing_df = show_missing_value_stats(data, showplot=plots)
    filtered_cols = missing_df[missing_df['percent_missing'] > MISSING_PERCENT_THRESHOLD].field.tolist()
    data.drop(filtered_cols, axis=1, inplace=True)

    #Identify categorical and numerical features in the data frame. Shouldn't hardcode column names(????)
    categotical_cols = ['buildingqualitytypeid', 'heatingorsystemtypeid', 'propertycountylandusecode', 'fips', 'regionidcity', 
        'propertyzoningdesc', 'pooltypeid7', 'regionidzip', 'rawcensustractandblock', 'propertylandusetypeid', 'regionidcounty', 
        'airconditioningtypeid', 'regionidneighborhood', 'yearbuilt']
    numerical_cols = [x for x in data.columns if x not in categotical_cols]

    # Plot correlation matrix for numerical features to find common features
    if plots:
        plt.figure(figsize = (15,8))
        sns.heatmap(data=data[numerical_cols].corr(), annot=True, fmt=".1f")
        plt.show()
        plt.gcf().clear()

    # Eliminating these columns to after observing high covariance with existing columns
    drop_columns = ['finishedsquarefeet12','calculatedbathnbr','finishedsquarefeet15', 'fullbathcnt', 'finishedsquarefeet50']

    # Assuming N.A implies no pools
    index = data.pooltypeid7.isnull()
    data.loc[index,'pooltypeid7'] = 0

    index = data.poolcnt.isnull()
    data.loc[index,'poolcnt'] = 0

    # Dropping off columns with a very high % missing values. Might revisit and retain if needed
    drop_columns.extend(['finishedfloor1squarefeet', 'threequarterbathnbr', 'fireplacecnt', 'numberofstories',
        'airconditioningtypeid', 'garagetotalsqft', 'garagecarcnt', 'regionidneighborhood', 'heatingorsystemtypeid',
        'buildingqualitytypeid', 'unitcnt', 'propertyzoningdesc'])

    data.drop(drop_columns, axis=1, inplace=True)
    data = change_df_dtypes(data)

    #remove rows with null values
    return data.dropna(how='any',axis=0)

def change_df_dtypes(df):
    '''
    Fixes datatype issues in the dataframe
    df : dataframe
    returns: A new dataframe with fixed datatypes
    '''
    from sklearn import preprocessing
    for c, dtype in zip(df.columns, df.dtypes):
        if dtype == 'float64':
            df[c] = df[c].astype(np.float32) 
        elif dtype == 'int64':
            df[c] = df[c].astype(np.int32)
        elif dtype == 'object':
            label = preprocessing.LabelEncoder()
            label.fit(list(df[c].values))
            df[c] = label.transform(list(df[c].values))
    return df

# Function to analyse missing values. To be used later
def show_missing_value_stats(df, showplot=False):
    '''
    Provide information of missing data in the dataframe
    df : data frame
    showplot: Draw a bar plot of the % of missing values, if true
    returns: A new dataframe with information about missing values for each features
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(showplot, bool)

    percent_missing_df = pd.DataFrame()
    percent_missing_df = (df.isnull().sum(axis=0) * 100/len(df)).reset_index()
    percent_missing_df.columns = ['field', 'percent_missing']
    percent_missing_df = percent_missing_df.sort_values(by = 'percent_missing', ascending = False)

    if showplot:
        # Plot % missing values
        ax = sns.barplot(x='percent_missing', y='field', data=percent_missing_df)
        sns.set(rc = {'figure.figsize':(15,20)})
        ax.set_xlabel('percent missing', fontsize=15)
        ax.set_ylabel('Field')
    
    return percent_missing_df