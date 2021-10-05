import itertools
import random
from decimal import Decimal
from typing import Iterable, Tuple
from rest_framework import generics, serializers
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Team, Coach, Player, Game, OnCourt, ScoreBoard, Tournament
from .serializers import GameSerializer, PlayerSerializer
from .consts import *

# === Registration and login ====
# when loging in or reegestrating we automaticly redirect to
# the coachs team data page.
# The query will cache all players data
# TODO: (front) hide players data andn add onclick for each player to show data


def login_page(request):
    """
    login for coaches
    username is the teams name
    and the password is the one the coach registerd with
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api/coach/' + username)
        else:
            messages.info(request, "state name or password is incorrect")
    context = {}
    return render(request, 'login.html', context)


def register(request):
    """
    TODO: modify UserCreationForm with a class that will have our own relevant fields
    registration for coaches as their team name
    Enter the team name you coach and write the password twice.
    Press submit to register Coach user
    and then login
    """
    teams = Team.objects.values('name').order_by('name')
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            team_name = form.cleaned_data.get('username')
            id = Team.objects.filter(name=team_name)
            id = list(id)[0].name
            form.save()
            messages.success(request, 'New coach in DB !' + id)
            return redirect('/api/coach/' + id)
        else:
            print(form.errors.keys)
    context = {'form': form, 'teams': list(teams)}
    return render(request, 'register.html', context)

# === The tournament games ===
# entry point is at 'api/'
# button will redirect to games_table page
# when redirecting the server will simulate ***THE ENTIRE TOURNEMENT***
# and will update the relevant tables (Game, OnCoart, Player)
# at the end the server will return all relevant data for the entire tournament
# TODO: (back) find a better way to update tables in a bulck and not in a for loop
# TODO: (front) Find a better looking presentation for the data


def get_games_btn(req):
    """
    rendering the first page
    """
    return render(req, 'index.html', {'name': 'Shai'})


def get_games(req):
    if not Coach.objects.exists():
        create_teams_and_coaches()
    if not Player.objects.exists():
        create_all_players_randomly()
    players = Player.objects.select_related('Team__coach').all()

    return render(req, "games_table.html", {"players": list(players)})


def get_team_data(request, name) -> render:
    team = Team.objects.get(name=name)
    players = Player.objects.filter(
        Team_id=1).order_by('first_name', 'last_name')
    return render(request, "team_data.html", {'team': team, 'players': list(players)})


def get_latest_tournamnet(request):
    tournament = Tournament.objects.last()
    games = Game.objects.select_related(
        'team_1', 'team_2', 'winning_team').filter(tournament_id=tournament.id)
    return render(request, "games_table.html", {'games': games, 'tournament': tournament.id})


# ===== Genarate Tournament =====

def generate_tournament(request):
    """
    This will select 8 random couples of the Teams and will create Games for them.
    """
    tournament = Tournament()
    tournament.save()
    pairs = []
    teams = list(Team.objects.all())
    random.shuffle(teams)
    for round, couples in ROUNDS.items():
        teams = play_round(teams, round, couples, tournament)

    games = Game.objects.select_related(
        'team_1', 'team_2', 'winning_team').filter(tournament_id=tournament.id)
    return render(request, "games_table.html", {'games': games, 'tournament': tournament.id})


def play_round(teams: list[int], round: str, couples: int, tournament: Tournament) -> list[int]:
    winners = []
    print(round, [team.name for team in teams])
    for i in range(0, len(teams) - 1, 2):
        team_1, team_2 = teams[i], teams[i+1]
        game = Game()
        game.team_1 = team_1
        game.team_2 = team_2
        game.tournament = tournament
        game.save()
        team_1_score, team_2_score, winner = play_game(game, team_1, team_2)
        game.team_1_score = team_1_score
        game.team_2_score = team_2_score
        game.winning_team = winner
        winners.append(winner)
        game.save()
    return winners


# ===== playing a game on server ======


def play_game(game: Game, team_1_id: int, team_2_id: int) -> Tuple[int, int, int]:
    """
    This function simulates a game:
    1. using update_playing_players_in_game()
        1.1. select players for both teams
        1.2. genarate players scores
        1.3. update onCourt table with this data.
        1.4. update Players table
    4. update total score of game
    5. return winner id
    """
    team_1_score, team_2_score = update_playing_players_in_game(
        team_1_id, team_2_id, game)

    if team_1_score > team_2_score:
        winner = team_1_id
    elif team_2_score > team_1_score:
        winner = team_2_id
    else:
        team_1_score += 1
        winner = team_1_id

    return team_1_score, team_2_score, winner


def update_playing_players_in_game(team_1_id: int, team_2_id: int, game: Game) -> Tuple[int, int]:
    """
    This will Query all players fropm both teams,
    randomize a list of random size in range(5-10) of playing players foro each tema
    and will update oncourt table with the relevant playing players and their (random)score
    """
    players = Player.objects.prefetch_related('Team').filter(
        Q(Team_id=team_1_id) | Q(Team_id=team_2_id)).order_by('Team_id')
    team1, team2 = list(players[:10]), list(players[10:])
    random.shuffle(team1)
    random.shuffle(team2)
    team1, team2 = team1[:random.randint(5, 10)], team2[:random.randint(5, 10)]

    team_1_total_score = 0
    team_2_total_score = 0
    players_scors = []  # collectiong these calculations for updating the players later

    # looping over two teams separately bc each team has different number of playing players
    # Creating OnCourt objects and updating table in bulk
    batch = []

    for player in team1:
        player_score = random.randint(0, 15)
        batch.append(OnCourt(player=player, game=game, score=player_score))
        team_1_total_score += player_score
        players_scors.append(
            (player.id, player_score, player.number_of_played_games, player.average_score))

    for player in team2:
        player_score = random.randint(0, 15)
        batch.append(OnCourt(player=player, game=game, score=player_score))
        team_2_total_score += player_score
        players_scors.append(
            (player.id, player_score, player.number_of_played_games, player.average_score))

    OnCourt.objects.bulk_create(batch, batch_size=len(batch))
    # updating players
    for id, score, played_games, avg in players_scors:
        new_avg = Decimal((avg + score) / (played_games + 1))
        Player.objects.filter(pk=id).update(
            number_of_played_games=played_games + 1,
            average_score=new_avg)

    return team_1_total_score, team_2_total_score


# ==== genarete data for empty tables ====

def create_teams_and_coaches():
    names = [(i, j)
             for i, j in itertools.product(FIRST_NAMES, LAST_NAMES) if i]
    random.shuffle(names)
    for i in range(NUM_OF_TEAMS):
        Coach.objects.create(first_name=names[i][0],
                             last_name=names[i][1])
    teams = STATE_NAMES.copy()
    random.shuffle(teams)
    for i, team_name in enumerate(teams[:16]):
        Team.objects.create(
            name=team_name, number_of_players=10, coach_id=i+1)


def create_all_players_randomly():
    # TODO: find a way to push all data in one query
    names = [(i, j)  # TODO: Maybe change the names selection with a loop that chooses NUM_OF_PLAYERS items
             for i, j in itertools.product(FIRST_NAMES, LAST_NAMES) if i]
    random.shuffle(names)
    heights = [Decimal(random.randrange(MIN_HEIGHT, MAX_HEIGHT)
                       )/100 for i in range(NUM_OF_PLAYERS)]
    for i in range(NUM_OF_PLAYERS):
        create_player(names[i][0], names[i][1],
                      heights[i], (i % NUM_OF_TEAMS) + 1)


def create_player(first, last, height, team_id):
    Player.objects.create(
        first_name=first,
        last_name=last,
        height=height,
        average_score=Decimal(0.0),
        number_of_played_games=0,
        Team_id=team_id)
