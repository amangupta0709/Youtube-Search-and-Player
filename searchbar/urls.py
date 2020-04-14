from django.urls import path
from searchbar import views

urlpatterns = [
    path('', views.videodata),
    path('<str:videoid>',views.player, name='player'),
]