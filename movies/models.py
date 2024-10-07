from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def next_year():
    return datetime.now().year + 1


class Movie(models.Model):
    class Meta:
        get_latest_by = 'release_year'
        indexes = [
            models.Index(fields=['release_year', 'rating', 'genre'])
        ]
        ordering = ['-rating', 'title']
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    GENRE_CHOICES = [
        ('comedy', 'comedy'),
        ('drama', 'drama'),
        ('tragedy', 'tragedy'),
        ('cartoon', 'cartoon'),
        ('adventure', 'adventure')
    ]

    poster = models.ImageField(upload_to='posters')
    title = models.CharField(max_length=256)
    release_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1895),
            MaxValueValidator(next_year),
        ]
    )
    description = models.CharField(max_length=2048)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    genre = models.CharField(max_length=32, choices=GENRE_CHOICES)
