
from django.urls import path
from .views import category_list, book_list, download_book

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', book_list, name='book_list'),
    path('download/<int:book_id>/', download_book, name='download_book'),
]
