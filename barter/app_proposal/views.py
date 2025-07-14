from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from app_proposal import forms, models
from app_ads.models import AdsItem
from app_proposal.models import ExchangeProposal


class ProposalSendListView(generic.ListView):
    models = ExchangeProposal
    template_name = "proposal/proposal_list.html"
    paginate_by = 3
    extra_context = {
        "title": "Исходящие запросы",
        "is_sending": True
    }

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_receiver=self.request.user).all()


class ProposalReceiveListView(generic.ListView):
    models = ExchangeProposal
    template_name = "proposal/proposal_list.html"
    queryset = ExchangeProposal.objects.all()
    paginate_by = 3
    extra_context = {
        "title": "Входящие запросы",
        "is_receiving": True
    }

    def get_queryset(self):
        return ExchangeProposal.objects.filter(ad_sender=self.request.user).all()


class ProposalCreateView(generic.CreateView):
    template_name = "proposal/proposal_request.html"
    form_class = forms.ExchangeProposalForm
    models = ExchangeProposal
    secondary_model = AdsItem
    success_url = reverse_lazy('app_proposal:list')

    def get_object(self, queryset=None):
        """Получает объект и проверяет права доступа."""
        obj = get_object_or_404(AdsItem, pk=self.kwargs.get('pk'))
        if obj.user == self.request.user:
            raise PermissionDenied("Вы не можете запрашивать обмен у себя самого")
        return obj

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context['item'] = self.get_object()
        # context.update(self.extra_context)
        return context

    def form_valid(self, form):
        form.instance.as_sender = self.request.user
        form.instance.status = models.ExchangeProposal.STATUS_CHOICES[0][0]
        return super().form_valid(form)


class ProposalDetail(generic.DetailView):
    model = ExchangeProposal
    template_name = "proposal/proposal_detail.html"


class ProposalStatusUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ExchangeProposal
    fields = []
    template_name = "proposal/proposal_confirm_update.html"
    new_status = None

    def dispatch(self, request, *args, **kwargs):
        proposal = self.get_object()
        print(proposal.ad_receiver)
        if self.request.user != proposal.ad_receiver:
            raise PermissionDenied("Вы не можете менять статус этого предложения.")
        if proposal.status != ExchangeProposal.STATUS_PENDING:
            raise PermissionDenied("Статус уже обновлен.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.status = self.new_status
        form.save()
        return redirect("app_proposal:detail", pk=self.object.pk)


class AcceptProposalView(ProposalStatusUpdateView):
    new_status = ExchangeProposal.STATUS_ACCEPTED


class RejectProposalView(ProposalStatusUpdateView):
    new_status = ExchangeProposal.STATUS_REJECTED
