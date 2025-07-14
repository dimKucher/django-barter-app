from django import forms

from app_proposal.models import ExchangeProposal


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['item', 'ad_receiver', 'ad_sender', 'comment'] #, 'status']

        # widgets = {
        #     'item': forms.TextInput(attrs={'class': 'form-control'}),
        #     'ad_sender': forms.TextInput(attrs={'class': 'form-control'}),
        #     'ad_receiver': forms.TextInput(attrs={'class': 'form-control'}),
        #     'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        #     # 'status': forms.Select(attrs={'class': 'form-control'}),
        # }

        labels = {
            'item': 'Товар для обмена',
            'ad_sender': 'Отправитель',
            'ad_receiver': 'Получатель',
            'comment': 'Комментарий к предложению обмена',
            'status': 'Состояние товара на обмен',
        }
