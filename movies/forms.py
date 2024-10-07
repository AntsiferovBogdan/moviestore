from datetime import datetime

from django import forms

from movies.models import Movie


class MovieAddForm(forms.Form):
    poster = forms.FileField(
        label='Постер',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    title = forms.CharField(
        label='Название фильма',
        max_length=256,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Минимум 2 символа'
            })
    )

    release_year = forms.IntegerField(
        label='Год выпуска',
        min_value=1895,
        max_value=datetime.now().year + 1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label='Описание',
        min_length=16,
        max_length=2048,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Минимум 16 символов'
            })
    )

    rating = forms.DecimalField(
        label='Рейтинг',
        min_value=0,
        max_value=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    genre = forms.ChoiceField(
        label='Жанр',
        choices=Movie.GENRE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        release_year = cleaned_data.get('release_year')

        if release_year > datetime.now().year:
            if rating:
                self.add_error('rating', 'Нельзя добавить фильму рейтинг, если он еще не выпущен')
        elif not rating:
            self.add_error('rating', 'Фильм уже выпущен, укажите рейтинг')


class MovieSearchForm(forms.Form):
    query = forms.CharField(
        label='Что ищем?',
        min_length=2,
        max_length=32,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или синопсису',
        })
        )
