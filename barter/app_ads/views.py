from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from app_ads import forms, models


class AdsCreate(CreateView):
    template_name = "ads/ads_form.html"
    form_class = forms.AdsItemForm
    success_url = reverse_lazy('main')
    extra_context = {
        "categories": models.AdsItem.CATEGORY_CHOICES,
        "conditions": models.AdsItem.CONDITION_CHOICES
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdsList(ListView):
    """Класс-представление для отображения списка."""

    model = models.AdsItem
    template_name = "ads/ads_list.html"
    context_object_name = "ads"

    # login_url = "/accounts/login/"
    # redirect_field_name = "login"

    def get_queryset(
            self, delivery_status: Optional[str] = None
    ) -> QuerySet[models.AdsItem]:
        """Функция возвращает queryset ."""
        try:
            ads = (
                models.AdsItem.objects.filter(user=self.request.user)
                .order_by("-created_at")
            )
            return ads
        except ObjectDoesNotExist:
            raise Http404("Объявлений нет")

    # def get(
    #         self,
    #         request: HttpRequest,
    #         status: Optional[str] = None,
    #         *args,
    #         **kwargs,
    # ) -> HttpResponse:
    #     """
    #     GET-функция для рендеренга списка заказов.
    #
    #     :param request: HttpRequest
    #     :param status: статус заказа
    #     """
    #     super().get(request, *args, **kwargs)
    #     if self.request.user.is_authenticated:
    #         queryset = self.get_queryset(delivery_status)
    #         object_list = MixinPaginator(
    #             queryset, request, self.paginate_by
    #         ).my_paginator()
    #     else:
    #         object_list = None
    #
    #     context = {
    #         "object_list": object_list,
    #     }
    #
    #     return render(request, self.template_name, context=context)
