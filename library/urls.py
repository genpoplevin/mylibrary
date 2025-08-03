from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('favorite/', views.favorite, name='favorite'),
    path(
        '<slug:category_slug>/',
        views.book_list,
        name='book_list_by_category',
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.book_detail,
        name='book_detail',
    ),
    path(
        'profile/<int:book_id>/follow/',
        views.book_follow,
        name='book_follow'
    ),
    path(
        'profile/<int:book_id>/unfollow/',
        views.book_unfollow,
        name='book_unfollow'
    ),
]
