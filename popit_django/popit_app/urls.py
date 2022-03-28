from django.urls import path
from popit_app import views


urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.hello_world, name='hello_world'),
]