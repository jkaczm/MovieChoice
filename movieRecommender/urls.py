from django.urls import path

from . import views

urlpatterns = [
    path('', views.app, name='app'),
    path('getMovieIds', views.getMovieIds),
    path('testJson', views.testJsonRequest),
    path('getRecommendations', views.getRecommendations),
]