# Generated by Django 3.0.3 on 2020-04-11 21:46

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0005_auto_20200331_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
