# Generated by Django 4.2.10 on 2024-03-07 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_blockrelation_friendship_matchhistory_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.TextField(),
        ),
    ]
