from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("upload-csv/", views.upload_csv, name="upload_csv"),
    path('upload-success/', views.upload_success, name='upload_success'),  # Страница успешной загрузки
    path('analyze/', views.analyze_files, name='analyze_files'),  # Страница анализа
]
