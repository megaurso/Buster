from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", views.UsersView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
]
