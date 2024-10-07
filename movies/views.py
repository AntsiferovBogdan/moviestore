from django.core.paginator import Page, Paginator
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from movies.models import Movie, next_year
from movies.forms import MovieAddForm, MovieSearchForm


def add_movie_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = MovieAddForm(request.POST, request.FILES)
        if form.is_valid():
            movie = Movie(
                poster=form.cleaned_data['poster'],
                title=form.cleaned_data['title'],
                release_year=form.cleaned_data['release_year'],
                description=form.cleaned_data['description'],
                rating=form.cleaned_data['rating'],
                genre=form.cleaned_data['genre'],
            )
            movie.save()
            return redirect('movie_info', movie_id=movie.id)
    else:
        form = MovieAddForm()
    return render(
        request,
        'add_movie.html',
        {'title': 'Добавить фильм', 'form': form},
    )


def get_movie_info_view(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=movie_id)
    title = movie.title
    return render(
        request,
        'movie_info.html',
        {'title': title, 'movie': movie},
    )


def paginate_queryset(request: HttpRequest, queryset: QuerySet[Movie], per_page: int = 4) -> Page:
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def search_form_view(request: HttpRequest) -> HttpResponse:
    title = 'Поиск фильма'
    form = MovieSearchForm()
    return render(
        request,
        'search.html',
        {'title': title, 'form': form},
    )


def search_movie_view(request: HttpRequest) -> HttpResponse:
    form = MovieSearchForm(request.GET)
    page_obj = None
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            movies = Movie.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            if movies:
                page_obj = paginate_queryset(request, movies)

    return render(
        request,
        'catalogue.html',
        {'page_obj': page_obj, 'show_filters': False},
    )


def show_catalogue_view(request: HttpRequest) -> HttpResponse:
    title = 'Каталог'

    rating = request.GET.get('rating')
    genres = request.GET.get('genres')
    decade = request.GET.get('decade')

    movies = Movie.objects.all()

    if rating:
        movies = movies.filter(rating__gte=rating)
    if genres:
        movies = movies.filter(genre__icontains=genres)
    if decade:
        decade_start = int(decade)
        decade_end = decade_start + 9
        movies = movies.filter(release_year__range=(decade_start, decade_end))

    page_obj = paginate_queryset(request, movies)

    all_ratings = list(range(1, 11))
    all_genres = set(Movie.objects.values_list('genre', flat=True))
    all_decades = list(range(1890, next_year(), 10))

    return render(request, 'catalogue.html', {
        'title': title,
        'page_obj': page_obj,
        'all_ratings': all_ratings,
        'all_genres': all_genres,
        'all_decades': all_decades,
        'selected_rating': rating,
        'selected_genres': genres,
        'selected_decade': decade,
        'show_filters': True,
    })
