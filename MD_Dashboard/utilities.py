import numpy as np
import pandas as pd
import re

def calculate_std(data: pd.DataFrame, column_1: str, column_2: str) -> tuple[float, float]:
    '''
    Function that calculates standard deviation for chosen columns
    :param data:
    :param column_1:
    :param column_2:
    :return:
    '''
    std_1 = data[column_1].std()
    std_2 = data[column_2].std()
    return std_1, std_2


def calculate_quantiles(data: pd.DataFrame, column_1: str, column_2: str) -> tuple[float, float, float, float]:
    '''
    Function created to calculate quantiles in data before and after imputation.
    :param data:
    :param column_1:
    :param column_2:
    :return:
    '''
    first_qauntile_1 = np.percentile(data[column_1], 25)
    first_qauntile_2 = np.percentile(data[column_2], 25)
    third_qauntile_1 = np.percentile(data[column_1], 75)
    third_qauntile_2 = np.percentile(data[column_2], 75)
    return first_qauntile_1, first_qauntile_2, third_qauntile_1, third_qauntile_2


def calculate_min_max(data: pd.DataFrame, column_1: str, column_2: str) -> tuple[float, float, float, float]:
    '''
    Function which calculates min and max for provided columns.
    :param data:
    :param column_1:
    :param column_2:
    :return:
    '''
    min_1 = data[column_1].min()
    max_1 = data[column_1].max()
    min_2 = data[column_2].min()
    max_2 = data[column_2].max()
    return min_1, max_1, min_2, max_2


def changing_to_npnan(data_imputation: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    Function that takes care of changing missing value to np.nan
    :param data_imputation:
    :param column:
    :return: data_imputation[column]
    '''
    data_imputation[column] = np.where((data_imputation[column] == 0) | (data_imputation[column] is None), np.nan, data_imputation[column])
    return data_imputation[column]


def calcualte_the_missing_percent_of_values(data: pd.DataFrame) -> list:
    '''
    Calculating how the precenteg of missing numbers
    :param data:
    :return: tuple with the name of the column and the percentage of missing values
    '''
    percent_missing = round(data.isnull().sum() * 100 / len(data), 2)
    missing_value_df = pd.DataFrame({'column_name': data.columns, 'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    missing_value_df['missing percent name'] = list(zip(missing_value_df.column_name, missing_value_df.percent_missing))
    missing_value_df['missing percent name'] = missing_value_df['missing percent name'].astype(str)
    return missing_value_df['missing percent name'].to_list()


def remove_unneeded_characters(percent_missing: list):
    new_percent_missing = []
    for element in percent_missing:
        element = re.sub('[^a-zA-Z0-9 \n\.]', '', element)
        new_percent_missing.append(element + '%')
    return new_percent_missing


