from dataclasses import dataclass
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404

from app_proposal import models


@dataclass
class ProposalFilterParams:
    """Контейнер для параметров фильтрации предложений обмена"""
    me: auth_models.User
    sender: Optional[auth_models.User] = None
    status: str = ""
    order_by: str = "-created_at"


def get_all_senders(me):
    """
    Возвращает всех уникальных пользователей
    во входящих запросах на обмен.
    """

    try:
        # для Postgres

        # models.ExchangeProposal.objects
        #     .filter(ad_receiver=me)
        #     .distinct()

        # для SQLite
        all_senders_id = set(
            (models.ExchangeProposal.objects
             .filter(ad_receiver=me)
             .values_list('ad_sender__id', flat=True).all())
        )
        uniq_sender_list = (
            auth_models.User.objects
            .filter(id__in=all_senders_id)
            .values_list('id', 'username')
        )
        return uniq_sender_list
    except ObjectDoesNotExist:
        raise Http404("Предложений нет")


class ProposalFilterService:
    """Сервис для фильтрации предложений обмена"""

    def __init__(self, filter_params: ProposalFilterParams):
        self.params = filter_params
        self.base_queryset = (
            models.ExchangeProposal.objects
            .filter(
                Q(ad_sender=self.params.me) |
                Q(ad_receiver=self.params.me)
            )
            .order_by(self.params.order_by)
        )

    def _apply_user_filter(self):
        """Фильтрация по пользователю"""
        if self.params.sender:
            return self.base_queryset.filter(ad_sender__username=self.params.sender)
        return self.base_queryset

    def _apply_status_filter(self, queryset):
        """Фильтрация по статусу предложения"""
        if self.params.status:
            return queryset.filter(status=self.params.status)
        return queryset

    def get_filtered_proposal(self):
        """Основной метод для получения отфильтрованных предложений"""
        try:
            queryset = self._apply_user_filter()
            queryset = self._apply_status_filter(queryset)
            return queryset
        except ObjectDoesNotExist:
            raise Http404("Предложений нет")
