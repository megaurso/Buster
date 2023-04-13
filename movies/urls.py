from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.MovieView.as_view()),
    path("movies/<int:movie_id>/", views.MovieInfoView.as_view()),
    path("movies/<int:movie_id>/orders/", views.PurchaseMovie.as_view())
]
