from django.urls import path, re_path
from . import views

app_name = 'engine'
urlpatterns = [
    path('', views.admin, name='admin'),
    re_path('search', views.search, name='search'),
    re_path('display', views.display, name='display'),
    re_path('detail', views.detail, name='detail')
]