# Generated by Django 3.2.4 on 2022-11-17 19:11

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0007_alter_court_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='court',
        ),
        migrations.AddField(
            model_name='court',
            name='case',
            field=models.ForeignKey(null=True, on_delete=django.db.models.expressions.Case, to='register.case', verbose_name='sprawa'),
        ),
    ]
