from django.urls import path

from . import views

urlpatterns = [
    # path("send-game-resutls", views.GameResutls.as_view(), name="send-game-resutls"),
    path("get-top-rank", views.GetTopRank.as_view(), name="get-top-rank"),
    path("get-my-rank/<int:account_id>", views.GetMyRank.as_view(), name="get-my-rank"),
    path("get-history/<int:account_id>", views.GetHistory.as_view(), name="get-history"),
    path("get-game-info/<int:game_id>", views.GetResultGame.as_view(), name="get-game-info"),
]
