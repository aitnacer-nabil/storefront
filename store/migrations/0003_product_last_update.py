# Generated by Django 5.0.4 on 2024-04-22 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_price_product_unit_price_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]