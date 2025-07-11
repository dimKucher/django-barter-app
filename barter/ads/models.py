from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class AdsItem(models.Model):
    """Модель объявления."""

    CATEGORY_CHOICES = [
        ('ELECTRONICS', 'Электроника'),
        ('CLOTHING', 'Одежда'),
        ('BOOKS', 'Книги'),
        ('HOME', 'Для дома'),
        ('OTHER', 'Другое'),
    ]

    CONDITION_CHOICES = [
        ('NEW', 'Новый'),
        ('LIKE_NEW', 'Как новый'),
        ('USED', 'Б/у'),
        ('DEFECT', 'С дефектами'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads_items',
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        allow_unicode=False,
        verbose_name="Slug"
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    image_url = models.ImageField(
        upload_to='items/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='OTHER',
        verbose_name='Категория'
    )
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        default='USED',
        verbose_name='Состояние'
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
        db_table = "app_ads"
        ordering = ["-created_at"]
        verbose_name = "объявление"
        verbose_name_plural = "объявления"

    def __str__(self) -> str:
        return f'{self.title} (Пользователь: {self.user.username})'

    def get_absolute_url(self) -> str:
        return reverse("ads:detail", kwargs={"pk": self.pk})


    # def save(self, *args, **kwargs) -> None:
    #     if not self.slug:
    #         self.slug = slugify_for_cyrillic_text(self.title)
    #     return super().save(*args, **kwargs)

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'ожидает'),
        ('ACCEPTED', 'принята'),
        ('REJECTED', 'отклонена'),
    ]
    ad_sender = models.ForeignKey(
        AdsItem,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name='Отправитель'
    )
    ad_receiver = models.ForeignKey(
        AdsItem,
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
                    ad_sender=self.ad_receiver,
                    ad_receiver=self.ad_sender
            ).exists():
                raise ValidationError("Обратное предложение уже существует")