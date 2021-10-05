from django.db.models.query_utils import RegisterLookupMixin
from django.urls import path

from . import views

# URL Conf
urlpatterns = [
    # preessing on the button will genarate a tournamnet
    path('', views.get_games_btn),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('games/', views.get_latest_tournamnet),
    path('genarate/', views.generate_tournament),
    path('coach/<str:name>/', views.get_team_data),
]
