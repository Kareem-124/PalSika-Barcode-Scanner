# Generated by Django 4.2.1 on 2024-10-03 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=13, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('customer_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
