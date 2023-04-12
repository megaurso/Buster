from django.shortcuts import render
from rest_framework.views import APIView, Response, Request, status
from users.models import User
from django.contrib.auth import authenticate
from users.serializers import UserSerializer


class UsersView(APIView):
    def get(self, req: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
