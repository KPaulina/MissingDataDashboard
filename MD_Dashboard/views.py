import os.path

import numpy as np
import pandas as pd
from django.shortcuts import render
import plotly.graph_objects as go
import plotly.express as px
from sklearn.impute import SimpleImputer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data\\')
# Create your views here.


def calculate_std(data, column_1, column_2):
    std_1 = data[column_1].std()
    std_2 = data[column_2].std()
    return std_1, std_2


def imputation_strategy(imput_strategy, data, context, column_1, column_2):
    context['column1'] = column_1
    context['column2'] = column_2
    context['imputation_strategy'] = imput_strategy
    if imput_strategy == 'mean' or imput_strategy == 'median':
        data_imputation = data.copy(deep=True)
        data_imputation = data_imputation[[column_1, column_2]]
        data_imputation[column_1] = np.where((data_imputation[column_1] == 0) | (data_imputation[column_1] is None), np.nan, data_imputation[column_1])
        data_imputation[column_2] = np.where((data_imputation[column_2] == 0) | (data_imputation[column_2] is None), np.nan, data_imputation[column_2])
        col = data_imputation.columns
        imputer = SimpleImputer(missing_values=np.nan, strategy=imput_strategy)
        data_imputation = pd.DataFrame(imputer.fit_transform(data_imputation))
        data_imputation.columns = col
        data_imputation.index = data.index

        return data_imputation, context
    data_imputation = data.copy(deep=True)
    data_imputation[column_1] = np.where((data_imputation[column_1] == 0) | (data_imputation[column_1] is None), np.nan, data_imputation[column_1])
    data_imputation[column_2] = np.where((data_imputation[column_2] == 0) | (data_imputation[column_2] is None), np.nan, data_imputation[column_2])
    mean_imputer = SimpleImputer(missing_values=np.nan, strategy=imput_strategy)
    data_imputation = pd.DataFrame(mean_imputer.fit_transform (data_imputation))
    data_imputation.columns = data.columns
    data_imputation.index = data.index

    return data_imputation, context


def data_from_csv(request):
    def create_chart(data, column_1, column_2):
        column_in_the_graph_1 = data[column_1]
        column_in_the_graph_2 = data[column_2]
        fig2 = px.scatter(data,
                           x=column_in_the_graph_1,
                           y=column_in_the_graph_2,
                           )
        box_plot_fig = go.Figure ()
        box_plot_fig.add_trace(go.Box(y=column_in_the_graph_1, name=column_1))
        box_plot_fig.add_trace(go.Box(y=column_in_the_graph_2, name=column_2))

        chart = box_plot_fig.to_html()
        chart2 = fig2.to_html()
        return chart, chart2
    name = 'diabetes'
    data = pd.read_csv(f'{DATA_DIR}{name}.csv', sep=',')
    column_names = data.columns.values.tolist()

    context = {'column_names': column_names}
    if request.method == "POST":
        column_1 = request.POST.get('column1')
        column_2 = request.POST.get('column2')
        std_1, std_2 = calculate_std(data, column_1, column_2)
        context['std1'] = std_1
        context['std2'] = std_2
        impu_strategy = request.POST.get('imputation')
        print(type(impu_strategy))
        data_imputation, context = imputation_strategy(impu_strategy, data, context, column_1, column_2)
        std_im_1, std_im_2 = calculate_std(data, column_1, column_2)
        data['std_imputation_1'] = std_im_1
        data['std_imputation_2'] = std_im_2
        chart_imputation_1, chart_imputation_2 = create_chart(data_imputation, column_1, column_2)
        context['chart_imputation_1'] = chart_imputation_1
        context['chart_imputation_2'] = chart_imputation_2
        chart, chart2 = create_chart(data, column_1, column_2)
        context['chart'] = chart
        context['chart2'] = chart2
        context['dashboard_created'] = True
        context['dashboard_not_created'] = False
        context['error'] = 'This imputation strategy cannot be used here'
    return render(request, 'data_display/display_columns.html', context)


def create_dashboard(request):
    pass
