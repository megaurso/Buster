from rest_framework.views import APIView, Response, Request, status
from movies.models import Movie
from movies.serializer import MovieSerializer, PurchaseMovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class RequestPermission(BasePermission):
    def has_permission(self, req, view):
        if req.method in ["POST", "DELETE"]:
            return bool(req.user.is_authenticated and req.user.is_superuser)
        return True


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RequestPermission]

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all().order_by("title")
        result_page = self.paginate_queryset(movies, req)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        user = User.objects.filter(id=req.user.id).first()

        serializer = MovieSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RequestPermission]

    def get(self, req: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseMovie(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = PurchaseMovieSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie, user=req.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
