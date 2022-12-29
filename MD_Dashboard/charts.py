import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_charts_for_one_column(data: pd.DataFrame, column: str):
    df = data[column]
    fig = px.box(df, y=column)
    chart = fig.to_html()
    return chart


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
    fig2 = px.scatter (data,
                       x=column_in_the_graph_1,
                       y=column_in_the_graph_2,
                       )
    box_plot_fig = go.Figure()
    box_plot_fig.add_trace(go.Box(y=column_in_the_graph_1, name=column_1))
    box_plot_fig.add_trace(go.Box(y=column_in_the_graph_2, name=column_2))

    chart = box_plot_fig.to_html()
    chart2 = fig2.to_html()
    return chart, chart2
