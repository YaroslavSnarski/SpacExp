import os, sys, csv
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import FileAnalysis
from django.db.models import Count, F, Q, Sum
from django.db import models 
from django.http import HttpResponse



# Убедитесь, что директория существует перед сохранением файла
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)

# Добавляем путь к модулю SpacExp
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SpacExp'))))
from SpacExp.file_manager import FileManager

def index(request):
    total_size_gb = FileAnalysis.objects.aggregate(total_size=models.Sum('file_size'))['total_size'] or 0
    total_size_gb = total_size_gb / (1024 ** 3)  # Перевод в гигабайты
    return render(request, 'index.html', {'total_size_gb': total_size_gb})

def select_folder(request):
    if request.method == 'POST':
        directory = request.POST.get('directory')

        if not directory:
#            output_csv = os.path.join(settings.MEDIA_ROOT, 'analysis_results.csv')
#            manager = FileManager(directory, output_csv)
#            manager.run()  # Анализ файлов
#            manager.import_csv_to_db(output_csv)  # Обновление базы данных
            return render(request, 'select_folder.html', {'error': 'Пожалуйста, выберите папку для анализа.'})


        # Запуск анализа
        output_csv = os.path.join(settings.MEDIA_ROOT, 'analysis_results.csv')
        manager = FileManager(directory, output_csv)
        manager.run()  # Анализ файлов
        manager.import_csv_to_db(output_csv)  # Обновление базы данных

        return redirect('analytics')  # Редирект на аналитику

    return render(request, 'select_folder.html')

def analytics(request):
    # Общая статистика
    files_by_extension = FileAnalysis.objects.values('extension').annotate(count=models.Count('id'))
    largest_files = FileAnalysis.objects.order_by('-file_size')[:10]
    largest_images = FileAnalysis.objects.filter(image_width__isnull=False, image_height__isnull=False).order_by('-image_width', '-image_height')[:10]
    documents_by_pages = FileAnalysis.objects.filter(num_pages__isnull=False).order_by('-num_pages')[:10]

    context = {
        'files_by_extension': files_by_extension,
        'largest_files': largest_files,
        'largest_images': largest_images,
        'documents_by_pages': documents_by_pages,
    }

    return render(request, 'analytics.html', context)
