import os.path
from .forms import MissingDataForm, OneColumnImputation
from .imputation_strategies import imputation_strategy_for_one_column, imputation_strategy
from .charts import create_charts_for_one_column, create_chart
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from .utilities import calculate_std, calculate_quantiles, calculate_min_max, calcualte_the_missing_percent_of_values, remove_unneeded_characters
from django.conf import settings
from django.core.files.storage import FileSystemStorage

'''
TO DO: check if there is a better method to read data from media directory, pagination of the table
'''


def the_number_of_columns_choice(request):
    '''
    Function created to give user a choice for how many columns imputations is to be done
    :param request:
    :return: display the page or redirect to the chosen page
    '''
    fss = FileSystemStorage()
    data = fss.open('data', mode='rb')
    data = pd.read_csv(data, sep=',')
    data.replace(0, np.nan, inplace=True)
    column_names = data.columns.values.tolist()
    percent_missing = calcualte_the_missing_percent_of_values(data)
    percent_missing = remove_unneeded_characters(percent_missing)
#     table = data.style.set_table_attributes('class="pure-table"')
#     table = table.highlight_null('yellow')
#     table = table.to_html(index=False)
    context = {'column_names': column_names, 'percent_missing': percent_missing}
    choice = request.GET.get("choice")
    if choice == 'one':
        return redirect('one-column')
    elif choice == 'two':
        return redirect('two-columns')
    return render(request, 'data_display/display_columns.html', context)


def data_from_csv(request):
    '''
    Function that takes data from csv, displays columns and shows charts for this data before and after imputation
    :param request:
    :return:
    '''

    fss = FileSystemStorage()
    data = fss.open('data', mode='rb')
    data = pd.read_csv(data, sep=',')
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
            std_1, std_2 = calculate_std(data, column_1, column_2)
            quantiles_1, quantiles_2, third_qauntile_1, third_qauntile_2 = calculate_quantiles(data, column_1,
                                                                                                column_2)
            min_1, max_1, min_2, max_2 = calculate_min_max (data, column_1, column_2)
            data_imputation = imputation_strategy(impu_strategy, data, column_1, column_2)
            std_im_1, std_im_2 = calculate_std (data_imputation, column_1, column_2)
            context.update()
            chart_imputation_1, chart_imputation_2 = create_chart (data_imputation, column_1, column_2)
            context['chart_imputation_1'] = chart_imputation_1
            context['chart_imputation_2'] = chart_imputation_2
            quantiles_im_1, quantiles_im_2, third_qauntile_im_1, third_qauntile_im_2 = calculate_quantiles (
                data_imputation, column_1, column_2)
            context.update({})
            imputation_min_1, imputation_max_1, imputation_min_2, imputation_max_2 = calculate_min_max (data_imputation,
                                                                                                        column_1,
                                                                                                        column_2)
            context.update({'imputation_min_1': imputation_min_1, 'imputation_max_1': imputation_max_1, 'std1': std_1, 'std2': std_2,
                            'imputation_min_2': imputation_min_2, 'imputation_max_2': imputation_max_2, 'std_imputation1': std_im_1, 'std_imputation2': std_im_2,
                            'first_quantile_im_1': quantiles_im_1, 'first_quantile_im_2': quantiles_im_2, 'third_quantiles_im_1': third_qauntile_im_1,
                            'third_quantiles_im_2': third_qauntile_im_2, 'min_1': min_1, 'max_1': max_1, 'min_2': min_2, 'max_2': max_2,
                            'first_quantile_1': quantiles_1, 'first_quantile_2': quantiles_2, 'third_quantiles_1': third_qauntile_1,
                            'third_quantiles_2': third_qauntile_2})
            chart_scatter, chart_box_plot = create_chart(data, column_1, column_2)
            context['chart'] = chart_scatter
            context['chart2'] = chart_box_plot

    return render(request, 'data_display/two_columns.html', context)


def one_column_view(request):
    '''
    Function made to show charts when user wants imputation on only one column
    :param request:
    :return:
    '''
    # data = pd.read_csv(f'{DATA_DIR}{NAME}.csv', sep=',')
    fss = FileSystemStorage()
    data = fss.open('data', mode='rb')
    data = pd.read_csv(data, sep=',')
    column_names = data.columns.values.tolist()
    form = OneColumnImputation()
    context = {'column_names': column_names, 'form': form}
    if request.method == "POST":
        '''
        TO DO: table: 1st quantile, 3rd quantile, min, max
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

            context.update({'std': std, 'chart': chart, 'chart_after_imputation': chart_after_imputation, 'imputed_data': data_imputed})
            return render(request, 'data_display/column_one.html', context)
    return render(request, 'data_display/column_one.html', context)


def upload_csv_view(request):
    fss = FileSystemStorage()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            return render(request, 'data_display/error.html')
        file = request.FILES['myFile']
        if not file.name.endswith('.csv'):
            return render(request, 'data_display/error.html')
        file.name = 'data'
        if fss.exists(file.name):
            os.remove(os.path.join(settings.MEDIA_ROOT, file.name))
        file = fss.save(file.name, file)
        return redirect('index')
    return render(request, 'data_display/upload.html')


