from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page of the products app
    path('details/', views.details, name='details'),  # Details page
]