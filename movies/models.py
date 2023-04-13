from django.db import models


class Movie(models.Model):
    RATING_CHOICES = [
        ("G", "G"),
        ("PG", "PG"),
        ("PG-13", "PG-13"),
        ("R", "R"),
        ("NC-17", "NC-17"),
    ]
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, null=True, default=None)
    rating = models.CharField(
        max_length=20, choices=RATING_CHOICES, default="G", blank=True, null=True
    )
    synopsis = models.TextField(blank=True, null=True, default=None)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )

    movies_order = models.ManyToManyField(
        "users.User",
        related_name="movies_order",
        through="movies.MovieOrder",
    )

    def __str__(self) -> str:
        return f"<Movie {self.id} = {self.title}]>"


class MovieOrder(models.Model):
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="order_movies"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_movies"
    )

    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"<MovieOrder {self.id} = {self.price}]>"
