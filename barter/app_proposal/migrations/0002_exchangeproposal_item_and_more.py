# Generated by Django 5.2.4 on 2025-07-14 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_ads", "0001_initial"),
        ("app_proposal", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="exchangeproposal",
            name="item",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item_for_exchange",
                to="app_ads.adsitem",
                verbose_name="товар для бартера",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="exchangeproposal",
            name="ad_receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receive_proposals",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Получатель",
            ),
        ),
        migrations.AlterField(
            model_name="exchangeproposal",
            name="ad_sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sender_proposals",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Отправитель",
            ),
        ),
    ]
