# Generated by Django 3.0.3 on 2020-05-24 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0009_remove_reservation_transfercar'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='time',
            field=models.TimeField(blank=True, default='11:11'),
            preserve_default=False,
        ),
    ]
