# Generated by Django 4.2.1 on 2024-12-31 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanapp', '0015_product_exported_qty_product_imported_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_id', models.IntegerField(default=0)),
            ],
        ),
    ]
