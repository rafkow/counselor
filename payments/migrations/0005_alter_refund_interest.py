# Generated by Django 3.2.4 on 2023-02-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_alter_payments_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='interest',
            field=models.FloatField(default=0, null=True, verbose_name='odsetki'),
        ),
    ]
