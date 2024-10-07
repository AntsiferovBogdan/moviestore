# Generated by Django 5.1.1 on 2024-10-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'get_latest_by': 'release_year', 'ordering': ['-rating', 'title'], 'verbose_name': 'movie', 'verbose_name_plural': 'movies'},
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
