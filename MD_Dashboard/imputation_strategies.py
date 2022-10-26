import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
import sklearn.neighbors._base
import sys
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest


def imputation_strategy(imput_strategy: str, data: pd.DataFrame, column_1: str, column_2: str) -> pd.DataFrame:
    '''
    Function that takes care of impute strategy on data
    :param imput_strategy:
    :param data:
    :param context:
    :param column_1:
    :param column_2:
    :return: data_imputation, context
    '''
    data_imputation = data.copy(deep=True)
    data_imputation[column_1] = changing_to_npnan(data_imputation, column_1)
    data_imputation[column_2] = changing_to_npnan(data_imputation, column_2)
    if imput_strategy == 'MissForest':
        imputer = MissForest()
        miss_data = imputer.fit_transform(data_imputation)
        miss_forest_data = pd.DataFrame(miss_data, columns=data.columns).round(1)
        return miss_forest_data
    elif imput_strategy == 'mean' or imput_strategy == 'median':
        data_imputation = data_imputation[[column_1, column_2]]
        col = data_imputation.columns
        imputer = SimpleImputer(missing_values=np.nan, strategy=imput_strategy)
        data_imputation = pd.DataFrame(imputer.fit_transform(data_imputation))
        data_imputation.columns = col
        data_imputation.index = data.index
        return data_imputation

    mean_imputer = SimpleImputer(missing_values=np.nan, strategy=imput_strategy)
    data_imputation = pd.DataFrame(mean_imputer.fit_transform (data_imputation))
    data_imputation.columns = data.columns
    data_imputation.index = data.index
    return data_imputation


def imputation_strategy_for_one_column(imput_strategy: str, data: pd.DataFrame, column: str):
    '''
            Function that takes care of impute strategy on data
            :param imput_strategy:
            :param data:
            :param context:
            :param column_1:
            :param column_2:
            :return: data_imputation, context
            '''
    data['index1'] = data.index
    data_imputation = data.copy(deep=True)
    data_imputation[column] = changing_to_npnan(data_imputation, column)
    if imput_strategy == 'MissForest':
        imputer = MissForest()
        miss_data = imputer.fit_transform(data_imputation)
        miss_forest_data = pd.DataFrame(miss_data, columns=data.columns).round(1)
        return miss_forest_data
    elif imput_strategy == 'mean' or imput_strategy == 'median':
        data_imputation = data_imputation[[column, 'index1']]
        col = data_imputation.columns
        imputer = SimpleImputer(missing_values=np.nan, strategy=imput_strategy)
        data_imputation = pd.DataFrame(imputer.fit_transform(data_imputation))
        data_imputation.columns = col
        data_imputation.index = data.index
        return data_imputation

    mean_imputer = SimpleImputer(missing_values=np.nan, strategy=imput_strategy)
    data_imputation = pd.DataFrame(mean_imputer.fit_transform(data_imputation))
    print('Old df')
    print(data.info())
    print(f'New data imputed df')
    print(data_imputation.info())
    data_imputation.columns = data.columns
    data_imputation.index = data.index
    return data_imputation


def changing_to_npnan(data_imputation: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    Function that takes care of changing missing value to np.nan
    :param data_imputation:
    :param column:
    :return: data_imputation[column]
    '''
    data_imputation[column] = np.where((data_imputation[column] == 0) | (data_imputation[column] is None), np.nan, data_imputation[column])
    return data_imputation[column]
