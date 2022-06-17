import os.path

import numpy as np
import pandas as pd
from django.shortcuts import render
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
from sklearn.impute import SimpleImputer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data\\')
# Create your views here.


def data_from_csv(request):
    def create_chart(data, column_1, column_2):
        column_in_the_graph_1 = data[column_1]
        column_in_the_graph_2 = data[column_2]
        fig2 = px.scatter (data,
                           x=column_in_the_graph_1,
                           y=column_in_the_graph_2,
                           )
        box_plot_fig = go.Figure ()
        box_plot_fig.add_trace (go.Box (y=column_in_the_graph_1, name=column_1))
        box_plot_fig.add_trace (go.Box (y=column_in_the_graph_2, name=column_2))

        chart = box_plot_fig.to_html ()
        chart2 = fig2.to_html ()
        return chart, chart2
    name = 'diabetes'
    data = pd.read_csv(f'{DATA_DIR}{name}.csv', sep=',')
    column_names = data.columns.values.tolist()

    context = {'column_names': column_names}
    if request.method == "POST":
        column_1 = request.POST.get('column1')
        column_2 = request.POST.get('column2')
        std_1 = data[column_1].std()
        std_2 = data[column_1].std()
        context['std1'] = std_1
        context['std2'] = std_2
        imputation_strategy = request.POST.get('imputation')
        if imputation_strategy == 'mean' or imputation_strategy == 'median':
            context['column1'] = column_1
            context['column2'] = column_2
            context['imputation_strategy'] = imputation_strategy
            data_imputation = data.copy(deep=True)
            # data[column_1].replace('', np.nan, inplace=True)
            # data_imputation[column_1] = pd.to_numeric(data[column_1], errors='coerce')
            # data_imputation[column_1] = data_imputation[column_1].astype(float)
            data_imputation = data_imputation[[column_1, column_2]]
            std_imputation_1 = data_imputation[column_1].std()
            std_imputation_2 = data_imputation[column_1].std()
            context['std_imputation_1'] = std_imputation_1
            context['std_imputation_2'] = std_imputation_2
            col = data_imputation.columns
            mean_imputer = SimpleImputer(missing_values=np.nan, strategy=imputation_strategy)

            data_imputation = pd.DataFrame(mean_imputer.fit_transform(data_imputation))
            data_imputation.columns = col
            data_imputation.index = data.index


            data_imputation[column_1] = np.where((data_imputation[column_1] == 0) | (data_imputation[column_1] is None), np.nan, data_imputation[column_1])
            chart_imputation_1, chart_imputation_2 = create_chart(data_imputation, column_1, column_2)
            context['chart_imputation_1'] = chart_imputation_1
            context['chart_imputation_2'] = chart_imputation_2
        else:
            context['column1'] = column_1
            context['column2'] = column_2
            context['imputation_strategy'] = imputation_strategy
            data_imputation = data.copy(deep=True)
            mean_imputer = SimpleImputer (missing_values=np.nan, strategy=imputation_strategy)

            data_imputation = pd.DataFrame (mean_imputer.fit_transform (data_imputation))
            data_imputation.columns = data.columns
            data_imputation.index = data.index

            data_imputation[column_1] = np.where (
                (data_imputation[column_1] == 0) | (data_imputation[column_1] is None), np.nan,
                data_imputation[column_1])
            chart_imputation_1, chart_imputation_2 = create_chart (data_imputation, column_1, column_2)
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
