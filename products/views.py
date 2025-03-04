from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from . import views

def index(request):
    products = Product.objects.all().order_by('ranking')
    return render(request, 'index.html', {'products': products})
    #return HttpResponse("Hello, world. You're at the products index.")

def details(request):
    return HttpResponse("You're looking at details")
    