import os.path

import sklearn

from .forms import MissingDataForm
import numpy as np
import pandas as pd
from django.shortcuts import render
import plotly.graph_objects as go
import plotly.express as px
from sklearn.impute import SimpleImputer
import sklearn.neighbors._base
import sys
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base
from missingpy import MissForest


'''
path to were data is stored
'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data\\')
# Create your views here.


def calculate_std(data: pd.DataFrame, column_1: str, column_2: str) -> tuple:
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


def calculate_quantiles(data: pd.DataFrame, column_1: str, column_2: str) -> tuple:
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


def calculate_min_max(data: pd.DataFrame, column_1: str, column_2: str) -> tuple:
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


def data_from_csv(request):
    '''
    Function that takes data from csv, displays columns and shows charts for this data before and after imputation
    :param request:
    :return:
    '''
    def create_chart(data: pd.DataFrame, column_1: str, column_2: str) -> tuple:
        '''
        Function that creates charts for the data
        :param data:
        :param column_1:
        :param column_2:
        :return:
        '''
        column_in_the_graph_1 = data[column_1]
        column_in_the_graph_2 = data[column_2]
        fig2 = px.scatter(data,
                           x=column_in_the_graph_1,
                           y=column_in_the_graph_2,
                           )
        box_plot_fig = go.Figure()
        box_plot_fig.add_trace(go.Box(y=column_in_the_graph_1, name=column_1))
        box_plot_fig.add_trace(go.Box(y=column_in_the_graph_2, name=column_2))

        chart = box_plot_fig.to_html()
        chart2 = fig2.to_html()
        return chart, chart2
    name = 'diabetes'
    data = pd.read_csv(f'{DATA_DIR}{name}.csv', sep=',')
    column_names = data.columns.values.tolist()
    form = MissingDataForm()
    context = {'column_names': column_names, 'form': form}
    if request.method == "POST":
        form = MissingDataForm(request.POST)
        impu_strategy = request.POST.get('imputation')
        context.update({'impu_strategy': impu_strategy, 'text': 'Before imputation', 'dashboard_created': True, 'dashboard_not_created': False, 'error': 'This imputation strategy cannot be used here'})
        if form.is_valid():
            column_1 = form.cleaned_data.get('column_1')
            column_2 = form.cleaned_data.get('column_2')
            context['column1'] = column_1
            context['column2'] = column_2
            # columns_object = MissingDataForm.objects.create(column_1=column_1, column_2=column_2)
            std_1, std_2 = calculate_std(data, column_1, column_2)
            context.update({'std1': std_1, 'std2': std_2})
            quantiles_1, quantiles_2, third_qauntile_1, third_qauntile_2 = calculate_quantiles(data, column_1, column_2)
            context.update({'first_quantile_1': quantiles_1, 'first_quantile_2': quantiles_2, 'third_quantiles_1': third_qauntile_1, 'third_quantiles_2': third_qauntile_2})
            min_1, max_1, min_2, max_2 = calculate_min_max(data, column_1, column_2)
            context.update({'min_1': min_1, 'max_1': max_1, 'min_2': min_2, 'max_2': max_2})
            data_imputation = imputation_strategy(impu_strategy, data, column_1, column_2)
            std_im_1, std_im_2 = calculate_std(data_imputation, column_1, column_2)
            context.update({'std_imputation1': std_im_1, 'std_imputation2': std_im_2})
            chart_imputation_1, chart_imputation_2 = create_chart(data_imputation, column_1, column_2)
            context['chart_imputation_1'] = chart_imputation_1
            context['chart_imputation_2'] = chart_imputation_2
            quantiles_im_1, quantiles_im_2, third_qauntile_im_1, third_qauntile_im_2 = calculate_quantiles(data_imputation, column_1, column_2)
            context.update({'first_quantile_im_1': quantiles_im_1, 'first_quantile_im_2': quantiles_im_2, 'third_quantiles_im_1': third_qauntile_im_1, 'third_quantiles_im_2':third_qauntile_im_2})
            imputation_min_1, imputation_max_1, imputation_min_2, imputation_max_2 = calculate_min_max(data_imputation, column_1, column_2)
            context.update({'imputation_min_1': imputation_min_1, 'imputation_max_1': imputation_max_1, 'imputation_min_2': imputation_min_2, 'imputation_max_2': imputation_max_2})
            chart, chart2 = create_chart(data, column_1, column_2)
            context['chart'] = chart
            context['chart2'] = chart2
    return render(request, 'data_display/display_columns.html', context)


