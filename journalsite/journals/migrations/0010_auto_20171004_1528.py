# Generated by Django 2.0.dev20170827005745 on 2017-10-04 04:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0009_auto_20171004_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='published_date',
            field=models.DateField(default=datetime.date(2017, 10, 4), verbose_name='published date'),
        ),
    ]