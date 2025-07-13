from typing import Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from app_ads import forms, models


class AdsCreate(LoginRequiredMixin, CreateView):
    """Класс-представление для создания товара."""

    template_name = "ads/ads_form.html"
    form_class = forms.AdsItemForm
    success_url = reverse_lazy('main')
    extra_context = {
        "categories": models.AdsItem.CATEGORY_CHOICES,
        "conditions": models.AdsItem.CONDITION_CHOICES,
        "title": "Новое объявление"
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdsList(ListView):
    """Класс-представление для отображения списка всех товаров."""
    model = models.AdsItem
    template_name = "ads/ads_list.html"
    paginate_by = 5
    extra_context = {
        "title": "Список всех товаров",
        "empty_message": "Тут ничего нет 🙁"
    }

    def get_queryset(self) -> QuerySet[models.AdsItem]:
        """Функция возвращает список товаров из БД."""
        try:
            if self.request.user.is_authenticated:
                object_list = (models.AdsItem.objects
                               .exclude(user=self.request.user)
                               .order_by("-created_at"))
            else:
                object_list = (models.AdsItem.objects
                               .order_by("-created_at"))
            return object_list
        except ObjectDoesNotExist:
            raise Http404("Объявлений нет")


class AdsUserList(LoginRequiredMixin, AdsList):
    """Класс-представление для отображения списка товаров пользователя."""

    model = models.AdsItem
    template_name = "ads/ads_list.html"
    paginate_by = 5
    extra_context = {
        "title": "Список ваших товаров",
        "empty_message": "Тут ничего нет 🙁"
    }

    def get_queryset(self) -> QuerySet[models.AdsItem]:
        """Функция возвращает список товаров из БД."""
        try:
            return (models.AdsItem.objects
                    .filter(user=self.request.user)
                    .order_by("-created_at"))
        except ObjectDoesNotExist:
            raise Http404("Объявлений нет")


class AdsDetail(DetailView):
    model = models.AdsItem
    template_name = "ads/ads_detail.html"


class AdsUpdate(UpdateView):
    """Класс для редактирования объявления."""
    model = models.AdsItem
    form_class = forms.AdsItemForm
    template_name = 'ads/ads_form.html'

    extra_context = {
        "title": "Редактирование объявления",
        "categories": models.AdsItem.CATEGORY_CHOICES,
        "conditions": models.AdsItem.CONDITION_CHOICES
    }

    def get_object(self, queryset=None):
        """Получает объект и проверяет права доступа."""
        obj = get_object_or_404(models.AdsItem, pk=self.kwargs.get('pk'))
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не можете редактировать это объявление")
        return obj

    def form_valid(self, form):
        """Дополнительная обработка при успешной валидации формы."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class AdsDelete(LoginRequiredMixin, DeleteView):
    model = models.AdsItem
    template_name = 'ads/ads_confirm_delete.html'
    success_url = reverse_lazy('app_ads:list_user')

    def get_object(self, queryset=None):
        """Получает объект и проверяет права доступа"""
        obj = get_object_or_404(models.AdsItem, pk=self.kwargs.get('pk'))
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить это объявление")
        return obj

    def delete(self, request, *args, **kwargs):
        """Добавляет сообщение об успешном удалении"""
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Объявление успешно удалено')
        return response

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение удаления'
        return context
