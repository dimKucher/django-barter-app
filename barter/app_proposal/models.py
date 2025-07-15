from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from app_ads.models import AdsItem


class ExchangeProposal(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'ожидает'),
        (STATUS_ACCEPTED, 'принята'),
        (STATUS_REJECTED, 'отклонена'),
    ]
    item = models.ForeignKey(
        AdsItem,
        on_delete=models.CASCADE,
        related_name='item_for_exchange',
        verbose_name='товар для бартера'
    )
    ad_sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender_proposals',
        verbose_name='Отправитель'
    )
    ad_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receive_proposals',
        verbose_name='Получатель'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Статус'
    )
    status_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='Сообщение к статусу'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего обновления'
    )

    objects = models.Manager()

    class Meta:
        db_table = "app_proposal"
        ordering = ["-created_at", '-updated_at']
        verbose_name = "предложение об обмене"
        verbose_name_plural = "предложения об обмене"

    def __str__(self):
        return f"Предложение {self.pk} [{self.get_status_display()}]"

    def clean(self):
        if self.ad_sender == self.ad_receiver:
            raise ValidationError("Нельзя создать предложение на тот же товар")

        if hasattr(self, 'ad_sender') and hasattr(self, 'ad_receiver'):
            if ExchangeProposal.objects.filter(
                    item=self.item,
                    ad_sender=self.ad_receiver,
                    ad_receiver=self.ad_sender
            ).exists():
                raise ValidationError("Обратное предложение уже существует")