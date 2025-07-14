from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from app_ads import forms, models, services


class AdsCreate(LoginRequiredMixin, generic.CreateView):
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


class BaseAdsListView(generic.ListView):
    """Базовый класс для списка объявлений"""
    model = models.AdsItem
    template_name = "ads/ads_list.html"
    paginate_by = 5
    is_mine = False

    @staticmethod
    def get_extra_context():
        """Возвращает общий контекст для всех страниц списка"""
        return {
            "categories": models.AdsItem.CATEGORY_CHOICES,
            "conditions": models.AdsItem.CONDITION_CHOICES,
            "empty_message": "Тут ничего нет 🙁"
        }

    def get_filter_params(self) -> services.AdsFilterParams:
        """Создает параметры фильтрации на основе запроса"""
        return services.AdsFilterParams(
            user=self.request.user,
            is_mine=self.is_mine,
            search_query=self.request.GET.get("search", ""),
            category_query=self.request.GET.get("category", ""),
            condition_query=self.request.GET.get("condition", ""),
            order_by="-created_at"
        )

    def get_queryset(self) -> QuerySet[models.AdsItem]:
        """Общий метод для получения отфильтрованного списка"""
        filter_params = self.get_filter_params()
        ads_service = services.AdsFilterService(filter_params)
        return ads_service.get_filtered_ads()

    def get_context_data(self, **kwargs):
        """Добавляет общий контекст"""
        context = super().get_context_data(**kwargs)
        context.update(self.get_extra_context())
        return context


class AdsList(BaseAdsListView):
    """Список всех товаров (кроме своих)"""
    extra_context = {"title": "Список всех товаров", }
    is_mine = False


class AdsUserList(LoginRequiredMixin, BaseAdsListView):
    """Список товаров пользователя"""
    extra_context = {"title": "Список ваших товаров", }
    is_mine = True


class AdsDetail(generic.DetailView):
    model = models.AdsItem
    template_name = "ads/ads_detail.html"


class AdsUpdate(generic.UpdateView):
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


class AdsDelete(LoginRequiredMixin, generic.DeleteView):
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
