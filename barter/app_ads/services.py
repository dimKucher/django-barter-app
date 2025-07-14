from dataclasses import dataclass
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404

from app_ads import models


@dataclass
class AdsFilterParams:
    """Контейнер для параметров фильтрации объявлений"""
    user: Optional[User] = None
    is_mine: bool = False
    search_query: str = ""
    category_query: str = ""
    condition_query: str = ""
    order_by: str = "-created_at"


class AdsFilterService:
    """Сервис для фильтрации объявлений"""

    def __init__(self, filter_params: AdsFilterParams):
        self.params = filter_params
        self.base_queryset = models.AdsItem.objects.filter(is_given=False).order_by(self.params.order_by)

    def _apply_user_filter(self):
        """Исключает объявления текущего пользователя"""
        if self.params.user and self.params.user.is_authenticated:
            if self.params.is_mine:
                return self.base_queryset.filter(user=self.params.user)
            else:
                return self.base_queryset.exclude(user=self.params.user)
        return self.base_queryset

    def _apply_search_filter(self, queryset):
        """Применяет поиск по тексту"""
        if self.params.search_query:
            return queryset.filter(
                Q(title__icontains=self.params.search_query) |
                Q(description__icontains=self.params.search_query)
            )
        return queryset

    def _apply_category_filter(self, queryset):
        """Фильтрация по категории"""
        if self.params.category_query:
            return queryset.filter(category=self.params.category_query)
        return queryset

    def _apply_condition_filter(self, queryset):
        """Фильтрация по состоянию"""
        if self.params.condition_query:
            return queryset.filter(condition=self.params.condition_query)
        return queryset

    def get_filtered_ads(self):
        """Основной метод для получения отфильтрованных объявлений"""
        try:
            queryset = self._apply_user_filter()
            queryset = self._apply_search_filter(queryset)
            queryset = self._apply_category_filter(queryset)
            queryset = self._apply_condition_filter(queryset)
            return queryset
        except ObjectDoesNotExist:
            raise Http404("Объявлений нет")
