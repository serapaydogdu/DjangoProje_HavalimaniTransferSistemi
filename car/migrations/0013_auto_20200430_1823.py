# Generated by Django 3.0.3 on 2020-04-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0012_auto_20200430_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='slug',
            field=models.SlugField(null='False', unique=True),
        ),
    ]
