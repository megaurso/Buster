from movies.models import Movie,MovieOrder
from rest_framework import serializers
from decimal import Decimal


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


class PurchaseMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.SerializerMethodField()
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.SerializerMethodField()

    def validate_price(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def get_buyed_by(self, obj):
        return obj.user.email
    
    def get_title(self,obj):
        return obj.movie.title

    def create(self, validated_data: dict) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
