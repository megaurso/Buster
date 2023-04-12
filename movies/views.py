from rest_framework.views import APIView, Response, Request, status
from movies.models import Movie
from movies.serializer import MovieSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
)
from users.models import User
from django.shortcuts import get_object_or_404


class RequestPermission(BasePermission):
    def has_permission(self, req, view):
        if req.method in ["POST", "DELETE"]:
            return bool(req.user.is_authenticated and req.user.is_superuser)
        return True


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [RequestPermission]

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

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
