# Generated by Django 4.2.10 on 2024-02-07 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameroom',
            name='guests',
        ),
        migrations.AddField(
            model_name='user',
            name='game_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='models.gameroom'),
        ),
        migrations.CreateModel(
            name='MatchHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('opponent_name', models.CharField(max_length=10)),
                ('result', models.CharField(max_length=10)),
                ('game_type', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_history', to='models.user')),
            ],
        ),
        migrations.CreateModel(
            name='BlockRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by_relations', to='models.user')),
                ('blocked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking_relations', to='models.user')),
            ],
        ),
    ]
