# Generated by Django 4.2.10 on 2024-03-07 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MatchHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('opponent_name', models.CharField(max_length=10)),
                ('result', models.CharField(max_length=10)),
                ('game_type', models.CharField(max_length=10)),
                ('match_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('oauth_id', models.IntegerField(default=0)),
                ('nick_name', models.CharField(default='', max_length=15)),
                ('total_win', models.IntegerField(default=0)),
                ('total_lose', models.IntegerField(default=0)),
                ('code', models.CharField(default='', max_length=6)),
                ('picture', models.CharField(blank=True, max_length=5000)),
                ('is_registered', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='gameroom',
            old_name='passWord',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='gameroom',
            name='guests',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='game_room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='models.gameroom'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='models.userprofile'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='models.userprofile'),
        ),
        migrations.AddField(
            model_name='matchhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_history', to='models.userprofile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='models.userprofile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships', to='models.userprofile'),
        ),
        migrations.AddField(
            model_name='blockrelation',
            name='blocked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by_relations', to='models.userprofile'),
        ),
        migrations.AddField(
            model_name='blockrelation',
            name='blocked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking_relations', to='models.userprofile'),
        ),
    ]
