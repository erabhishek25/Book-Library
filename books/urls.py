from django.urls import path

from .views import BookListView, upload_csv


urlpatterns = [

	path('', BookListView.as_view(), name='book_list'),
	path('csv/', upload_csv, name='upload_csv'),
]