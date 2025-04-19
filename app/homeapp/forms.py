from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import News, Partner


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'text': CKEditorWidget(),
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'min_context1', 'min_context2', 'min_context3', 'min_context4', 'context', 'photo']
