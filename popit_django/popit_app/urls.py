from django.urls import path
from popit_app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('game',views.game,name="game"),
    path('video_stream', views.video_stream, name='video_stream'),
    #path('', views.hello_world, name='hello_world'),
]