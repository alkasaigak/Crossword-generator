from django.urls import re_path
from django.conf.urls.static import static

from .views import (
    create_book_normal,
    BookListView,
)

app_name = 'store'

urlpatterns = [

    re_path(r'^book/create_normal', create_book_normal, name='create_book_normal'),
    re_path(r'^book/list', BookListView.as_view(), name='book_list'),

]
