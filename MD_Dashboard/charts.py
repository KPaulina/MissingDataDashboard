import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import pandas as pd
import missingno as msno


def create_charts_for_one_column(data: pd.DataFrame, column: str):
    df = data[column]
    fig = px.box(df, y=column)
    chart = fig.to_html()
    return chart


def bar_chart_showing_number_of_missing_data(df: pd.DataFrame):

    fig = px.bar(df, x='columns_names', y='number of nulls')
    return fig.to_html()
    # fig = px.histogram(df, x="number of nulls")
    # return fig
# column_in_the_graph_1 = data[column_1]
# column_in_the_graph_2 = data[column_2]
# fig2 = px.scatter (data,
#                    x=column_in_the_graph_1,
#                    y=column_in_the_graph_2,
#                    )
# box_plot_fig = go.Figure ()
# box_plot_fig.add_trace (go.Box (y=column_in_the_graph_1, name=column_1))
# box_plot_fig.add_trace (go.Box (y=column_in_the_graph_2, name=column_2))
#
# chart = box_plot_fig.to_html ()
# chart2 = fig2.to_html ()
# return chart, chart2
