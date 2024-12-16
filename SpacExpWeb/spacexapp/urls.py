from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('select-folder/', views.select_folder, name='select_folder'),  # Выбор папки
    path('analytics/', views.analytics, name='analytics'),  # Аналитика
]
