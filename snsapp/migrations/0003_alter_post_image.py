# Generated by Django 4.1.2 on 2022-12-07 07:27

from django.db import migrations, models
import snsapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('snsapp', '0002_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=snsapp.models.image_directry_path),
        ),
    ]