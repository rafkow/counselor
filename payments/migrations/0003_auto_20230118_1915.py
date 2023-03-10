# Generated by Django 3.2.4 on 2023-01-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payments_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='payment_date',
            field=models.DateTimeField(null=True, verbose_name='data spłaty'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='value',
            field=models.FloatField(null=True, verbose_name='spłacono'),
        ),
    ]
