from django import forms
from .models import AdsItem


class AdsItemForm(forms.ModelForm):
    class Meta:
        model = AdsItem
        fields = ['title', 'description', 'category', 'condition', 'image_url']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание', "row":2}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'image_url': forms.FileInput()
        }

        labels = {
            'title': 'Название товара',
            'description': 'Описание товара на обмен',
        }


