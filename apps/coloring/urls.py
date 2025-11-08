from django.urls import path
from . import views

app_name = 'coloring'

urlpatterns = [
    path('', views.coloring_list, name='coloring_list'),
    path('<int:coloring_id>/', views.coloring_detail, name='coloring_detail'),
]