import os

from django.conf import settings
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
        upload_to='media/items/',
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

    @property
    def image(self) -> str:
        """
        Метод возвращает URL-изображения категории.

        Возвращает URL-изображения
        или дефолтное изображение.
        """
        return os.path.join(settings.MEDIA_URL, self.image_url.url)

    # def save(self, *args, **kwargs) -> None:
    #     if not self.slug:
    #         self.slug = slugify_for_cyrillic_text(self.title)
    #     return super().save(*args, **kwargs)
