from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Team, Coach, Player, Game, OnCourt, ScoreBoard


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'team_1', 'team_2', 'team_1_score', 'team_2_score')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'height', 'average_score')
