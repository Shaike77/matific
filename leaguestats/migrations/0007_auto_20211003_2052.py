# Generated by Django 3.2.7 on 2021-10-03 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaguestats', '0006_auto_20211003_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='oncourt',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='number_of_played_games',
            field=models.PositiveIntegerField(),
        ),
    ]
