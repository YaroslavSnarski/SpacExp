from django.urls import path
from . import views
#from spacexapp import views  # Импортируем views из вашего приложения spacexapp

urlpatterns = [
    path('', views.index, name='index'),
    path("upload-csv/", views.upload_csv, name="upload_csv"),
    path('upload-success/', views.upload_success, name='upload_success'),  # Страница успешной загрузки
    path('analyze/', views.analyze_files, name='analyze_files'),  # Страница анализа
    path('scan_folder/', views.scan_folder, name='scan_folder'),  # Новый маршрут
    path('analyze_data/', views.analyze_data, name='analyze_data'),  # Новый маршрут для анализа данных
    path('statistics/', views.view_statistics, name='view_statistics'),  # Страница с анализом статистики
#    path('get_task_progress/<str:task_id>/', views.get_task_progress, name='get_task_progress'),  # Маршрут для прогресса
]
