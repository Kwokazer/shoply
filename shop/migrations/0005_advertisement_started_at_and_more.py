# Generated by Django 4.1.2 on 2023-02-25 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_historicalorder_historicalcomponent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='started_at',
            field=models.DateTimeField(null=True, verbose_name='Дата публикации'),
        ),
        migrations.AddField(
            model_name='historicaladvertisement',
            name='started_at',
            field=models.DateTimeField(null=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='archive_at',
            field=models.DateTimeField(null=True, verbose_name='Дата окончания публикации'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='historicaladvertisement',
            name='archive_at',
            field=models.DateTimeField(null=True, verbose_name='Дата окончания публикации'),
        ),
        migrations.AlterField(
            model_name='historicaladvertisement',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='shop.product', verbose_name='Товары в заказе'),
        ),
    ]