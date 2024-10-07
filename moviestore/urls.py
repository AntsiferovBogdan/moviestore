"""
URL configuration for moviestore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from movies import views
from moviestore.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('', lambda request: redirect('/search/')),
    path('admin/', admin.site.urls),
    path('catalogue/', views.show_catalogue_view, name='catalogue'),
    path('movies/<int:movie_id>/', views.get_movie_info_view, name='movie_info'),
    path('movies/add/', views.add_movie_view, name='add_movie'),
    path('search/', views.search_form_view, name='search_form'),
    path('search/results/', views.search_movie_view, name='search_movie'),
]


def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


handler404 = 'moviestore.urls.custom_page_not_found_view'


if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
