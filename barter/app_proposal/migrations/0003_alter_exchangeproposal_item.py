# Generated by Django 5.2.4 on 2025-07-15 01:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_ads", "0001_initial"),
        ("app_proposal", "0002_exchangeproposal_item_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchangeproposal",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="item_for_exchange",
                to="app_ads.adsitem",
                verbose_name="товар для бартера",
            ),
        ),
    ]
