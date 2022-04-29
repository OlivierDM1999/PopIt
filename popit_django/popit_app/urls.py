from django.urls import path
from popit_app import views


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
    path('inscription', views.inscription, name='inscription'),
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion',views.deconnexion, name='deconnexion'),
    path('jouer', views.jouer, name='jouer'),
    path('classement', views.classement, name='classement'),
    path('contact', views.contact, name='contact'),
    path('game',views.game,name="game"),
    path('game2',views.game2,name="game2"),
    path('video_stream', views.video_stream, name='video_stream'),
    #path('', views.hello_world, name='hello_world'),
]