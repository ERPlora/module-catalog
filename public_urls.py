from django.urls import path
from . import views

app_name = 'catalog_public'

urlpatterns = [
    path('', views.public_catalog, name='catalog'),
]
