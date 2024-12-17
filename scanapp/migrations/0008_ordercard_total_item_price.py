# Generated by Django 4.2.1 on 2024-12-17 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanapp', '0007_orderitem_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercard',
            name='total_item_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]