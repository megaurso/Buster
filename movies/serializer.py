from movies.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, required=False)
    rating = serializers.ChoiceField(
        choices=Movie.RATING_CHOICES, default="G", allow_null=True, required=False
    )
    synopsis = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    added_by = serializers.SerializerMethodField()

    def create(self, validated_data: dict) -> Movie:
        return Movie.objects.create(**validated_data)

    def get_added_by(self, obj):
        return obj.user.email

