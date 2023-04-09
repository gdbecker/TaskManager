from django import forms

from . import models
from taskapp.choices import *

class DateInput(forms.DateInput):
    input_type = 'date'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ('name',)

class ItemAddForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ('text', 'due_date', 'category',)
        widgets = {
            'due_date': DateInput()
        }

class FilterForm(forms.Form):
    date_sort = forms.ChoiceField(choices=DATE_SORT_CHOICES)
    category_sort = forms.ModelChoiceField(required=False, queryset=models.Category.objects.all())
    completed_sort = forms.ChoiceField(choices=STATUS_SORT_CHOICES)
