import os.path
import sklearn
from .forms import MissingDataForm, OneColumnImputation
from .imputation_strategies import imputation_strategy_for_one_column, imputation_strategy
from .charts import create_charts_for_one_column, bar_chart_showing_number_of_missing_data
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
import plotly.graph_objects as go
import plotly.express as px


'''
path to were data is stored
'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data\\')
'''
Name of your dataset in csv, do not add .csv ending
'''
NAME = 'diabetes'
# Create your views here.


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
    percent_missing = data.isnull().sum() * 100 / len(data)
    missing_value_df = pd.DataFrame({'column_name': data.columns, 'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    missing_value_df['missing percent name'] = list(zip(missing_value_df.column_name, missing_value_df.percent_missing))
    #[+-]?([0-9]*[.])?[0-9]+ floating point number regex
    return missing_value_df['missing percent name'].to_list()


def the_number_of_columns_choice(request):
    '''
    Function created to give user a choice for how many columns imputations is to be done
    :param request:
    :return: display the page or redirect to the chosen page
    '''
    data = pd.read_csv(f'{DATA_DIR}{NAME}.csv', sep=',')
    data.replace(0, np.nan, inplace=True)
    column_names = data.columns.values.tolist()
    percent_missing = calcualte_the_missing_percent_of_values(data)
    context = {'column_names': column_names, 'percent_missing': percent_missing}
    choice = request.GET.get("choice")
    if choice == 'one':
        return redirect(one_column_view)
    elif choice == 'two':
        return redirect(data_from_csv)
    return render(request, 'data_display/display_columns.html', context)


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
    data = pd.read_csv(f'{DATA_DIR}{NAME}.csv', sep=',')
    column_names = data.columns.values.tolist()
    form = MissingDataForm()
    context = {'column_names': column_names, 'form': form}
    if request.method == "POST":
        form = MissingDataForm(request.POST)
        impu_strategy = request.POST.get('imputation')
        context.update({'impu_strategy': impu_strategy, 'text': 'Before imputation', 'dashboard_created': True,
                         'dashboard_not_created': False, 'error': 'This imputation strategy cannot be used here'})
        if form.is_valid():
            column_1 = form.cleaned_data.get('column_1')
            column_2 = form.cleaned_data.get('column_2')
            context['column1'] = column_1
            context['column2'] = column_2
            # columns_object = MissingDataForm.objects.create(column_1=column_1, column_2=column_2)
            std_1, std_2 = calculate_std (data, column_1, column_2)
            context.update ({'std1': std_1, 'std2': std_2})
            quantiles_1, quantiles_2, third_qauntile_1, third_qauntile_2 = calculate_quantiles (data, column_1,
                                                                                                column_2)
            context.update ({'first_quantile_1': quantiles_1, 'first_quantile_2': quantiles_2,
                             'third_quantiles_1': third_qauntile_1, 'third_quantiles_2': third_qauntile_2})
            min_1, max_1, min_2, max_2 = calculate_min_max (data, column_1, column_2)
            context.update ({'min_1': min_1, 'max_1': max_1, 'min_2': min_2, 'max_2': max_2})
            data_imputation = imputation_strategy(impu_strategy, data, column_1, column_2)
            std_im_1, std_im_2 = calculate_std (data_imputation, column_1, column_2)
            context.update ({'std_imputation1': std_im_1, 'std_imputation2': std_im_2})
            chart_imputation_1, chart_imputation_2 = create_chart (data_imputation, column_1, column_2)
            context['chart_imputation_1'] = chart_imputation_1
            context['chart_imputation_2'] = chart_imputation_2
            quantiles_im_1, quantiles_im_2, third_qauntile_im_1, third_qauntile_im_2 = calculate_quantiles (
                data_imputation, column_1, column_2)
            context.update ({'first_quantile_im_1': quantiles_im_1, 'first_quantile_im_2': quantiles_im_2,
                             'third_quantiles_im_1': third_qauntile_im_1, 'third_quantiles_im_2': third_qauntile_im_2})
            imputation_min_1, imputation_max_1, imputation_min_2, imputation_max_2 = calculate_min_max (data_imputation,
                                                                                                        column_1,
                                                                                                        column_2)
            context.update ({'imputation_min_1': imputation_min_1, 'imputation_max_1': imputation_max_1,
                             'imputation_min_2': imputation_min_2, 'imputation_max_2': imputation_max_2})
            chart, chart2 = create_chart(data, column_1, column_2)
            context['chart'] = chart
            context['chart2'] = chart2

    return render(request, 'data_display/two_columns.html', context)


def how_many_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame({'number of nulls': data.isna().sum()})
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'columns_names'})
    return df


def one_column_view(request):
    '''
    Function made to show charts when user wants imputation on only one column
    :param request:
    :return:
    '''
    data = pd.read_csv(f'{DATA_DIR}{NAME}.csv', sep=',')
    column_names = data.columns.values.tolist()
    form = OneColumnImputation()
    context = {'column_names': column_names, 'form': form}
    if request.method == "POST":
        '''
        TO DO: imputation strategy, other stuff: 1st quantile, 3rd quantile, min, max
        '''
        form = OneColumnImputation(request.POST)
        impu_strategy = request.POST.get('imputation')
        context.update({'impu_strategy': impu_strategy, 'one': True, 'choice_if_one_or_two_columns': True, 'dashboard_created': True, 'error': 'This imputation strategy cannot be used here'})
        if form.is_valid():
            column = form.cleaned_data.get('column')
            context['column'] = column
            std = data[column].std()
            data_imputed = imputation_strategy_for_one_column(impu_strategy, data, column)

            chart = create_charts_for_one_column(data, column)
            chart_after_imputation = create_charts_for_one_column(data_imputed, column)

            missing_datanumbers = how_many_missing_values(data)
            print(missing_datanumbers.info())
            missing_data_chart = bar_chart_showing_number_of_missing_data(missing_datanumbers)
            context.update({'std': std, 'chart': chart, 'chart_after_imputation': chart_after_imputation, 'missing_data_chart': missing_data_chart})
    return render(request, 'data_display/column_one.html', context)

