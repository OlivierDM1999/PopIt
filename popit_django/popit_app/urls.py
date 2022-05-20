from django.urls import path
from popit_app import views


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
    path('inscription', views.inscription, name='inscription'),
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion',views.deconnexion, name='deconnexion'),
    path('jouer', views.jouer, name='jouer'),
    path('getDifficultes', views.getDifficultes, name='getDifficultes'),
    path('classement', views.classement, name='classement'),
    path('contact', views.contact, name='contact'),
    path('game',views.game,name="game"),
    path('game1',views.game1,name="game1"),
    path('game2',views.game2,name="game2"),

    path('gamefinal', views.gamefinal, name="gamefinal"),

    path('video_stream/', views.video_stream, name='video_stream1'),
    path('video_stream/<int:type_>', views.video_stream, name='video_stream'),
    path('mode_perso',views.mode_perso,name="mode_perso"),
    path('authentification',views.authentification,name='authentification'),
    path('checkAuth',views.checkAuth,name="checkAuth"),
]