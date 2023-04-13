# Generated by Django 4.2 on 2023-04-13 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0004_movieorder_movie_movies_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movieorder",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_movies",
                to="movies.movie",
            ),
        ),
    ]