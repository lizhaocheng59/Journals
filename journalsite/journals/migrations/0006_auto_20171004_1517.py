# Generated by Django 2.0.dev20170827005745 on 2017-10-04 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0005_auto_20171004_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='published_date',
            field=models.DateTimeField(default='DD-MM-YYYY', verbose_name='published date'),
        ),
    ]
