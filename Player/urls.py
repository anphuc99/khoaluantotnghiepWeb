from django.urls import path

from . import views

urlpatterns = [
    path("choose-character", views.ChooseCharaterAPI.as_view(), name="choose-character"),
    path("check-player", views.CheckPlayerAPI.as_view(), name="check-player"),
    path("set-multiplier", views.SetMultiplierAPI.as_view(), name="set-multiplier"),
    path("get-player", views.GetPlayer.as_view(), name="get-player"),
    
]
