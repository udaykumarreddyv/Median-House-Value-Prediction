import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from statsmodels.formula.api import ols
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
import pickle
import joblib
from scipy.stats import normaltest
import os.path


def data_modeling():
    '''
    This function will read in the clean_data_2016.csv, which is the output from the data_processing.py function which
    cleans the raw data. This function then performs K-Fold Cross Validation between 2 different regression models,
    namely Multiple Linear Regression and Random Forest Regression, built using train data and tests this on test data
    to compares the Mean Squared Error (MSE) of each model. The model with the lower MSE is chosen to model the Median
    House Value of houses given a set of predictors ('bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet',
    'latitude', 'longitude', 'poolcnt', 'regionidzip', 'yearbuilt', 'taxvaluedollarcnt') as input. Then we find the
    Median House Value for 3 data stories across a range of different Southern California zip codes. The 3 data stories
    are a 1 Bedroom/1 Bathroom home for a working professional, 2 Bedroom/2 Bathroom home for a working professional
    who wants to share with a roommate, and a 3 Bedroom/3 Bathroom home for a nuclear family (two parents and two
    children).
    :return: CSV containing Median House Value for 3 different data stories for a list of zip codes.
    '''

    assert isinstance('clean_data_2016.csv', str)  # Verify that the input file name is indeed a string
    assert len('clean_data_2016.csv') > 0  # Verify that the input file name provided is a valid file name (length > 0)

    # Loading the data
    initial_data = pd.read_csv('clean_data_2016.csv')

    # Extract the relevant columns
    data = initial_data[['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet', 'latitude', 'longitude',
                         'poolcnt', 'regionidzip', 'yearbuilt', 'taxvaluedollarcnt']]

    ### Part 1: Create the Multiple Linear Regression and Random Forest Regression models and then perform 5-fold
    # K-Fold cross-validation for both models. Report the mean test set MSE.
    data_part1 = data.copy()

    kf = KFold(n_splits=10, shuffle=True)
    kf.get_n_splits(data_part1)

    mse_multiple_linear_regression = []
    mse_random_forest_regression = []

    K = 0  # Iteration of K-Fold
    P = 8  # Number of predictors
    
    print('start model training')
    for train_index, test_index in kf.split(data_part1):
        # print("TRAIN:", train_index, "TEST:", test_index)
        data_train, data_test = data_part1.iloc[list(train_index), :], data_part1.iloc[list(test_index), :]

        ### Part 1. Multiple Linear Regression model: ###
        # Step 1: Fit the model to the training data, using predictor
        multiple_linear_formula = 'taxvaluedollarcnt ~ 1'
        for column_name in data.columns[0:8]:
            multiple_linear_formula += ' + '
            multiple_linear_formula += column_name

        multiple_linear_formula_model = ols(multiple_linear_formula, data_train).fit()

        # Step 2: Find the predicted values of the training set using the current model
        prediction_multiple_linear = multiple_linear_formula_model.predict(data_test)

        # Step 3: Find the MSE for the current model and save
        mse_multiple_linear_regression.append(
            mean_squared_error(data_test['taxvaluedollarcnt'], prediction_multiple_linear))

        print('Finished Multiple Linear Regression for %d' % (K))

        # Part 2. Random Forest model:
        # Step 1: Fit the model to the training data, using predictor
        rf = RandomForestRegressor(random_state=0)
        rf.fit(data_train.iloc[:, :P], data_train['taxvaluedollarcnt'])

        # Step 2: Find the predicted values of the training set using the current model
        rf_y_true = data_test['taxvaluedollarcnt']
        rf_y_pred = rf.predict(data_test.iloc[:, :P])

        # Step 3: Find the MSE for the current model and save
        mse_random_forest_regression.append(mean_squared_error(rf_y_true, rf_y_pred))

        print('Finished Random Forest Regression for %d' % (K))

        K += 1

    ### Part 2: Report the Average Mean Squared Error of each model.
    # print("Average MSE Multiple Linear Regression = ", sum(mse_multiple_linear_regression) / 10)
    # print("Average MSE Random Forest Regression = ", sum(mse_random_forest_regression) / 10)
    # print("Minimum Average MSE = ", min([sum(mse_multiple_linear_regression)/10, sum(mse_random_forest_regression)/10]))

    # Plot the Average Mean Squared Error's of each model.
    # plt.scatter(range(1, 10 + 1), mse_random_forest_regression, marker='o', color='blue',
#                label='Random Forest Regression')
    # plt.scatter(range(1, 10 + 1), mse_multiple_linear_regression, marker='o', color='green',
#                label='Multiple Linear Regreesion')
    # plt.title('MSE of Random Forest Regression versus Multiple Linear Regression')
    # plt.xlabel('Iteration # of K-Fold Cross Distribution')
    # plt.xticks(range(1, 10 + 1))
    # plt.ylabel('Mean-Squared Error')
    # plt.legend()
    # plt.grid()

    ### Part 3: Based on the results above, we conclude that random forest regressor is the better model.
    # Save the model to local and save the model as a pickle in a file
    joblib.dump(rf, 'my_rfr.pkl')

    # Load the model from the file
    # knn_from_joblib = joblib.load('filename.pkl')

    # Use the loaded model to make predictions
    # knn_from_joblib.predict(X_test)

    # Only load the model once
    # rf_from_joblib = joblib.load('my_rfr.pkl')
    

    # Repeat for Multiple Linear Regression model
    joblib.dump(multiple_linear_formula_model, 'my_mlfr.pkl')
    # mlfr_from_joblib = joblib.load('my_mlfr.pkl')
    # mlfr_from_joblib.predict(np.array([0, 0, 0, 0, 0, 0, 0, 0]).reshape(1, -1))

    ### Part 4: Use the model to predict the Median Home Value for 3 separate data stories.
    # To make our data stories relatable, we choose three fundamental family options:
    # a. Two bedrooms, two bathrooms housing for two to four college students.
    # b. One bedroom, one bathroom housing for one working professional.
    # c. Three bedrooms, three bathrooms housing for a family of two parents and two children.

    # For each zipcode, we create three corresponding samples, each of which has eight features. The squarefeet for
    # each housing option, we used the data from
    # a. For two bedrooms, two bathrooms apartment, the average squarefeet is 1030
    # b. For one bedroom, one bathroom apartment, the average squarefeet is 722
    # c. For three bedroom, two bathroom apartment, the average squarefeet is 1300

    # First find all the unique zipcodes in the original dataset
    zipcodes = list(initial_data.regionidzip.unique())

    # Next we look for the mean and median of three housing options from our own dataset.
    # Two bedrooms, two bathrooms housing:
    mean_two_two = data.loc[(data.bathroomcnt == 2.0) & (data.bedroomcnt == 2.0)].calculatedfinishedsquarefeet.mean()
    median_two_two = data.loc[(data.bathroomcnt == 2.0) & (data.bedroomcnt == 2.0)].calculatedfinishedsquarefeet.median()

   
   

    # One bedroom, one bathroom housing:
    mean_one_one = data.loc[(data.bathroomcnt == 1.0) & (data.bedroomcnt == 1.0)].calculatedfinishedsquarefeet.mean()
    median_one_one = data.loc[
        (data.bathroomcnt == 1.0) & (data.bedroomcnt == 1.0)].calculatedfinishedsquarefeet.median()

   

    

    

    # Three bedrooms and three bathrooms:
    mean_three_three = data.loc[
        (data.bathroomcnt == 3.0) & (data.bedroomcnt == 3.0)].calculatedfinishedsquarefeet.mean()
    median_three_three = data.loc[
        (data.bathroomcnt == 3.0) & (data.bedroomcnt == 3.0)].calculatedfinishedsquarefeet.median()

    

    # For latitude and longitude
    

    def zip_average_lat(zipcode):
        '''
        zipcode:
        '''
        return data.loc[data.regionidzip == zipcode].latitude.mean()

    def zip_average_lon(zipcode):
        '''
        zipcode:
        '''
        return data.loc[data.regionidzip == zipcode].longitude.mean()

    # For yearbuilt
    # ax = sns.displot(data.head(5000).loc[(data.bathroomcnt == 3.0) & (data.bedroomcnt == 3.0)].yearbuilt)

    median_year_built_33 = data.loc[(data.bathroomcnt == 3.0) & (data.bedroomcnt == 3.0)].yearbuilt.median()

    # ax = sns.displot(data.head(5000).loc[(data.bathroomcnt == 2.0) & (data.bedroomcnt == 2.0)].yearbuilt)

    median_year_built_22 = data.loc[(data.bathroomcnt == 2.0) & (data.bedroomcnt == 2.0)].yearbuilt.median()

    # ax = sns.displot(data.head(5000).loc[(data.bathroomcnt == 1.0) & (data.bedroomcnt == 1.0)].yearbuilt)

    median_year_built_11 = data.loc[(data.bathroomcnt == 1.0) & (data.bedroomcnt == 1.0)].yearbuilt.median()

    # For poolcnt
    # ax = sns.displot(data.head(5000).poolcnt)

    # Time to build our sample space for data stories!
    ds_X = []
    for z in zipcodes:
        new_1 = [1, 1, median_one_one, zip_average_lat(z), zip_average_lon(z), 0, z, median_year_built_11]
        new_2 = [2, 2, median_two_two, zip_average_lat(z), zip_average_lon(z), 0, z, median_year_built_22]
        new_3 = [3, 3, median_three_three, zip_average_lat(z), zip_average_lon(z), 0, z, median_year_built_33]
        ds_X.append(new_1)
        ds_X.append(new_2)
        ds_X.append(new_3)

    ds_y = []
    for x in ds_X:
        ds_y.append(rf.predict(np.array(x).reshape(1, -1)))

    result = []
    for i in range(len(ds_X)):
        new = ds_X[i]
        new.append(ds_y[i][0])
        result.append(new)

    # result

    final = pd.DataFrame(result, columns=['bathroomcnt', 'bedroomcnt', 'calculatedfinishedsquarefeet',
                                          'latitude', 'longitude', 'poolcnt', 'regionidzip', 'yearbuilt',
                                          'taxvaluedollarcnt'])

    if os.path.exists('./datastories_table.csv') == False:
        final.to_csv('datastories_table.csv')
    else:
        print('datastories_table.csv already exists.')


#    final.to_csv('datastories_table.csv')


