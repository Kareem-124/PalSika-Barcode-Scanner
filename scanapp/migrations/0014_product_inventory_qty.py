# Generated by Django 4.2.1 on 2024-12-21 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanapp', '0013_product_inventory_lower_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory_qty',
            field=models.IntegerField(default=0),
        ),
    ]
