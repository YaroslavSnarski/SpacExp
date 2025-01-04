from django.shortcuts import render
from .models import FileRecord
from django.conf import settings
from django.shortcuts import render
from django.db.models import Sum, Count, F
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import os
import sys
import tempfile
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SpacExp'))))
from SpacExp.file_manager import FileManagerWeb
from utils.gui_humanizer import humanize_file_size

@csrf_exempt
def process_files_view(request):
    if request.method == "POST":
        # получаем путь к папке из запроса
        folder_path = request.POST.get("folder_path", "").strip()

        # если путь к папке указан, проверяем валидность
        if folder_path:
            if not os.path.exists(folder_path):
                return render(request, "pages/error_page.html", {"error_message": "Несуществующий путь к папке."})
            
            # создаём FileManager для обработки файлов в папке
            file_manager = FileManagerWeb(folder_path)
            results = file_manager.process_files()

        else:
            # если путь не указан, обрабатываем загруженные файлы
            uploaded_files = request.FILES.getlist("files")
            if not uploaded_files:
                return render(request, "pages/error_page.html", {"error_message": "Вы не выбрали папку. Пожалуйста, выберите папку."})
            
            # создаём временную папку для хранения загруженных файлов
            with tempfile.TemporaryDirectory() as temp_dir:
                for file in uploaded_files:
                    file_path = os.path.join(temp_dir, file.name)
                    with open(file_path, "wb") as temp_file:
                        for chunk in file.chunks():
                            temp_file.write(chunk)
                
                # обрабатываем файлы в временной папке
                file_manager = FileManagerWeb(temp_dir)
                results = file_manager.process_files()

        # сохраняем результаты в базе данных
        FileRecord.objects.all().delete()
        for result in results:
            # убедимся, что 'type' присутствует
            if 'type' not in result:
                result['type'] = 'unknown'
            
            FileRecord.objects.create(
                file_path="N/A", 
                file_name=result["file_name"],
                file_size=result.get("file_size", 0),
                creation_time=result.get("creation_time", datetime.now()), 
                modification_time=result.get("modification_time", datetime.now()), 
                extension=os.path.splitext(result["file_name"])[1].lower(),
                type=result["type"],
                page_count=result.get("page_count"),
                width=result.get("width"),
                height=result.get("height"),
                area=result.get("area"),
                sheet_names=result.get("sheet_names"), 
            )

        return HttpResponseRedirect("/api/statistics-page/")
    return render(request, "pages/error_page.html", {"error_message": "Неверный метод запроса."})

def index(request):
    total_size = FileRecord.objects.aggregate(Sum('file_size'))['file_size__sum'] or 0  # размер файлов в байтах
    total_files = FileRecord.objects.count()  # количество файлов
#    total_size_gb = total_size / (1024 ** 3)  # размер в гигабайтах
    total_size_humanized = humanize_file_size(total_size)  # размер в читаемом формате

    return render(request, 'pages/index.html', {
        'total_size': total_size_humanized,
        'total_files': total_files
    })

def statistics_page_view(request):
    # статистика по расширениям
    file_statistics = FileRecord.objects.values("extension").annotate(count=Count("id")).order_by("-count")

    # Топ 10 самых больших файлов
    largest_files = FileRecord.objects.order_by("-file_size").values("file_name", "file_size")[:10]

    # топ 10 самых больших изображений
    largest_images = FileRecord.objects.filter(type="image").annotate(
        calculated_area=F("width") * F("height")
    ).order_by("-calculated_area").values("file_name", "width", "height", "calculated_area")[:10]

    # топ 10 документов по количеству страниц
    largest_documents = FileRecord.objects.filter(type="document", page_count__isnull=False).order_by(
        "-page_count"
    ).values("file_name", "page_count")[:10]

    # общий размер файлов
    total_size = FileRecord.objects.aggregate(Sum('file_size'))['file_size__sum'] or 0
    total_size_humanized = humanize_file_size(total_size)

    # чек на пустоту или None
    response_data = {
        "file_statistics": list(file_statistics),
        "largest_files": [
            {
                "file_name": file["file_name"],
                "file_size": humanize_file_size(file["file_size"]) if file["file_size"] else 0,
            }
            for file in largest_files
        ],
        "largest_images": [
            {
                "file_name": img["file_name"],
                "width": img["width"] if img["width"] else 0,
                "height": img["height"] if img["height"] else 0,
                "calculated_area": img["calculated_area"] if img["calculated_area"] else 0,
            }
            for img in largest_images
        ],
        "largest_documents": [
            {
                "file_name": doc["file_name"],
                "page_count": doc["page_count"] if doc["page_count"] else 0
            }
            for doc in largest_documents
        ],
        "total_size": total_size_humanized

    }

    return render(request, "pages/statistics.html", response_data)

def statistics_api_view(request):
    # статистика по расширениям, отсортированная по числу файлов (убывание)
    file_statistics = FileRecord.objects.values("extension").annotate(count=Count("id")).order_by("-count")

    # топ 10 самых больших файлов, независимо от расширения
    largest_files = FileRecord.objects.order_by("-file_size").values("file_name", "file_size")[:10]

    # топ 10 самых больших изображений (по площади)
    largest_images = FileRecord.objects.filter(type="image").annotate(
        calculated_area=F("width") * F("height")
    ).order_by("-calculated_area").values("file_name", "width", "height", "calculated_area")[:10]

    # топ 10 документов по количеству страниц
    largest_documents = FileRecord.objects.filter(type="document", page_count__isnull=False).order_by(
        "-page_count"
    ).values("file_name", "page_count")[:10]

    # данные для ответа
    response_data = {
        "file_statistics": list(file_statistics),
        "largest_files": [
            {
                "file_name": file["file_name"],
                "file_size": humanize_file_size(file["file_size"]),
            }
            for file in largest_files
        ],
        "largest_images": list(largest_images),
        "largest_documents": list(largest_documents),
    }

    return JsonResponse(response_data)
