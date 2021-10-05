from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField


class Tournament(models.Model):
    event_date = models.DateTimeField(auto_now=True)


class Coach(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_main = models.BooleanField(default=True)


class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    average_score = models.DecimalField(max_digits=5, decimal_places=1)
    number_of_played_games = models.PositiveIntegerField()
    played_games = models.ManyToManyField('Game', through='OnCourt')
    Team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, null=True, related_name='+')


class Team(models.Model):
    name = models.CharField(max_length=255)
    number_of_players = models.PositiveIntegerField()
    last_update = models.DateTimeField(auto_now=True)
    coach = models.OneToOneField(
        Coach, on_delete=models.PROTECT, primary_key=True)


class Game(models.Model):
    team_1 = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name='+')
    team_2 = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name='+')
    team_1_score = models.PositiveIntegerField(default=0)
    team_2_score = models.PositiveIntegerField(default=0)
    round = models.PositiveIntegerField(default=0)
    playing_players = models.ManyToManyField(Player, through='OnCourt')
    winning_team = models.ForeignKey(
        Team,  on_delete=models.SET_NULL, null=True, related_name='+')
    tournament = models.ForeignKey(
        Tournament, on_delete=models.SET_NULL, null=True, related_name='+')


class OnCourt(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)


class ScoreBoard(models.Model):
    games = models.ForeignKey(Game, on_delete=models.PROTECT)
