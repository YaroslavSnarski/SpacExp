from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-files/', views.process_files_view, name='process_files'),
    path("statistics/", views.statistics_api_view, name="statistics_api"),
    path('statistics-page/', views.statistics_page_view, name='statistics_page')
]
