# Generated by Django 4.2.10 on 2024-04-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.URLField(),
        ),
    ]
