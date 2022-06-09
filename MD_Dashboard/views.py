import os.path
import pandas as pd
from django.shortcuts import render
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data\\')
# Create your views here.


def data_from_csv(request):
    name = 'diabetes'
    data = pd.read_csv(f'{DATA_DIR}{name}.csv', sep=',')
    column_names = data.columns.values.tolist()
    context = {'column_names': column_names}
    if request.method == "POST":
        column_1 = request.POST.get('column1')
        column_2 = request.POST.get('column2')
        context['column1'] = column_1
        context['column2'] = column_2
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

        context['chart'] = chart
        context['chart2'] = chart2

        context['dashboard_created'] = True
    return render(request, 'data_display/display_columns.html', context)


def create_dashboard(request):
    pass
