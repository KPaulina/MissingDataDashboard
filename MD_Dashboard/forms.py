from django import forms


class MissingDataForm(forms.Form):
    column_1 = forms.CharField()
    column_2 = forms.CharField()

    def clean_column_1(self):
        cleaned_data = self.cleaned_data
        column_1 = cleaned_data.get('column_1')
        return column_1

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data


class OneColumnImputation(forms.Form):
    column = forms.CharField()

    def clean_column(self):
        cleaned_data = self.cleaned_data
        column = cleaned_data.get('column')
        return column

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data



