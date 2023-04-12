from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=127, write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already registered.")
        return value

    def create(self, validated_data: dict) -> User:
        is_employee = validated_data.get("is_employee", False)
        if is_employee:
            validated_data["is_superuser"] = True
        return User.objects.create_user(**validated_data)
