from django import forms

from app_proposal.models import ExchangeProposal


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['item', 'ad_receiver', 'ad_sender', 'comment']

        labels = {
            'item': 'Товар для обмена',
            'ad_sender': 'Отправитель',
            'ad_receiver': 'Получатель',
            'comment': 'Комментарий к предложению обмена',
        }
