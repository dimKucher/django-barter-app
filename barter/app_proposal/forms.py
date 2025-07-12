from django import forms

from app_proposal.models import ExchangeProposal


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment', 'status']

        widgets = {
            'ad_sender': forms.TextInput(attrs={'class': 'form-control'}),
            'ad_receiver': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'ad_sender': 'Отправитель',
            'ad_receiver': 'Получатель',
            'comment': 'Комментарий к предложению обмена',
            'status': 'Состояние товара на обмен',
        }
