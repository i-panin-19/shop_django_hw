# Generated by Django 5.0 on 2023-12-24 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория')),
                ('description', models.TextField(blank=True, max_length=400, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, max_length=400, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='office_shop/', verbose_name='Превью')),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Розничная цена')),
                ('date_creation', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_modified', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='office_shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'ordering': ['date_creation', 'name'],
            },
        ),
    ]
