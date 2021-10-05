# Generated by Django 3.2.7 on 2021-10-03 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaguestats', '0005_remove_team_players'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='playing_players',
        ),
        migrations.RemoveField(
            model_name='player',
            name='played_games',
        ),
        migrations.CreateModel(
            name='OnCourt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaguestats.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaguestats.player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='playing_players',
            field=models.ManyToManyField(through='leaguestats.OnCourt', to='leaguestats.Player'),
        ),
        migrations.AddField(
            model_name='player',
            name='played_games',
            field=models.ManyToManyField(through='leaguestats.OnCourt', to='leaguestats.Game'),
        ),
    ]