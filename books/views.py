import pandas as pd

from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Book
from .forms import FileForm



class BookListView(ListView):
	model = Book
	template_name = 'book_list.html'


def upload_csv(request):
	data = {}

	if request.method == 'GET':
		return render(request, 'books/upload_file.html')

	try:
		csv_file = request.FILES.get('csv_file')
		if not csv_file.name.endswith('.csv'):
			messages.error(request, 'File is not csv type')
			return HttpResponseRedirect(reverse('upload_csv'))

		file_data = csv_file.read().decode('utf-8')
		lines = file_data.split('\n')

		df = pd.read_csv(file_data)
		for line in lines:
			fields = line.split(',')
			data_dict = {}
			data_dict['title'] = fields[0]
			data_dict['author'] = fields[1]
			data_dict['genre'] = fields[2]
			data_dict['height'] = fields[3]
			data_dict['publisher'] = fields[4]

			try:
				form = FileForm(data_dict)
				if form.is_valid():
					form.save()
				else:
					messages.error(request, 'Invalid data!')
			except Exception as e:
				pass
 
	except Exception as e:
		messages.error(request,"Unable to upload file. "+repr(e))

	return HttpResponseRedirect(reverse('upload_csv'))
