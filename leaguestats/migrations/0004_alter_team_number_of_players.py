# Generated by Django 3.2.7 on 2021-10-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaguestats', '0003_player_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='number_of_players',
            field=models.PositiveIntegerField(),
        ),
    ]