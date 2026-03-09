from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Admin views (authentication required)
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
]
