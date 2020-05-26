#폼
from django import forms
from .models import SearchObj, SearchMeta

class searchForm(forms.ModelForm):
    class Meta:
        model = SearchMeta
        fields = ('key',)

