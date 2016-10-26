from django.shortcuts import render
from django.http import HttpResponse
from .models import sheeps_table

# Create your views here.
def index(request):
    return render(request, 'wellofsheep/index.html', {})

def table(request):
    sheeps = sheeps_table.objects.all()
    return render(request, 'wellofsheep/table.html', {'sheeps': sheeps})

def get_more_tables(request):
    sheeps = sheeps_table.objects.all()
    return render(request, 'wellofsheep/get_more_tables.html', {'sheeps': sheeps})
