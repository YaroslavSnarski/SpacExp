import csv
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .forms import CSVUploadForm
from .models import FileMetadata
from django.db.models import Count, F, Q, Sum
from django.db import transaction
import sys
import os
import shutil  # Для удаления папки
from .forms import FolderSelectionForm  # Форма для выбора папки
import pandas as pd
from spacexapp.models import FileAnalysis

# Добавляем путь к модулю SpacExp
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SpacExp'))))
from SpacExp.file_manager import FileManager  # Теперь можно импортировать FileManager
#def scan_folder(request):
#    files_data = []

#    if request.method == 'POST':
#        folder = request.FILES.get('folder')
#
#        if folder:
#            # Убедитесь, что папка существует, и создайте её при необходимости
#            temp_folder = os.path.join(settings.BASE_DIR, 'temp_uploads')  # Путь к временной папке
#            os.makedirs(temp_folder, exist_ok=True)  # Создаем папку, если её нет
#
#            # Сохраняем загруженные файлы во временную папку
#            folder_path = os.path.join(temp_folder, folder.name)  # Путь к файлу
#
#            # Сохраняем файл на диск
#            with open(folder_path, 'wb') as f:
#                for chunk in folder.chunks():
#                    f.write(chunk)

#            # Теперь передаем путь к файлу в FileManager для анализа
#            file_manager = FileManager(directory=temp_folder, output_file='output.csv')
#            file_manager.run()  # Выполняем сканирование папки

#            # Получаем результаты и передаем их в шаблон
#            files_data = file_manager.get_results()  # Замените на нужный метод

#            # После того как обработка завершена, удаляем временные файлы
#            shutil.rmtree(temp_folder)  # Удаляет всю временную папку и ее содержимое

#    return render(request, 'spacexapp/scan_folder.html', {'files_data': files_data})

# Представление для сканирования папки
def scan_folder(request):
    files_processed = False  # Флаг для отображения кнопки перехода на страницу статистики

    if request.method == 'POST' and 'folder_path' in request.POST:
        # Получаем путь к выбранной папке
        folder_path = request.POST['folder_path']
        
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Если путь существует и это папка, запускаем анализ
            output_file = 'output.csv'  # Можно указать путь для сохранения результатов
            file_manager = FileManager(folder_path, output_file)
            file_manager.run()  # Запуск обработки файлов
            
            files_processed = True  # Устанавливаем флаг успешной обработки

        else:
            return HttpResponse("Ошибка: выбранный путь не является существующей папкой.")
    
    # Если запрос GET, отображаем форму для выбора папки
    form = FolderSelectionForm()
    return render(request, 'spacexapp/scan_folder.html', {'form': form, 'files_processed': files_processed})

# Представление для анализа статистики
def view_statistics(request):
    # Читаем данные из CSV файла для анализа
    if os.path.exists('output.csv'):
        data = pd.read_csv('output.csv')
        # Тут можно произвести анализ данных, например:
        total_files = len(data)
        total_size = data['file_size'].sum()
        # Пример анализа данных
        context = {
            'total_files': total_files,
            'total_size': total_size,
            'data': data.head()  # Показать первые строки таблицы
        }
        return render(request, 'spacexapp/statistics.html', context)
    else:
        return HttpResponse("Ошибка: нет данных для анализа.")



def analyze_data(request):
    # Получаем все данные из базы данных
    files_data = FileAnalysis.objects.all()

    return render(request, 'spacexapp/analyze_data.html', {'files_data': files_data})



def index(request):
    return render(request, 'spacexapp/index.html')


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data["file"]
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file, delimiter=';')

            try:
                # Start a transaction block
                with transaction.atomic():
                    for row in reader:
                        # Validate and parse the datetime values
                        created_str = row.get("created", "").strip() if row.get("created") else ""
                        modified_str = row.get("modified", "").strip() if row.get("modified") else ""


                        # Parse datetime strings into datetime objects, handle invalid formats
                        created = None
                        modified = None
                        if created_str:
                            try:
                                created = parse_datetime(created_str)
                                if created:
                                    created = timezone.make_aware(created, timezone.get_default_timezone())
                            except ValueError:
                                print(f"Invalid 'created' date format for row: {row}")
                        if modified_str:
                            try:
                                modified = parse_datetime(modified_str)
                                if modified:
                                    modified = timezone.make_aware(modified, timezone.get_default_timezone())
                            except ValueError:
                                print(f"Invalid 'modified' date format for row: {row}")

                        # If created is still None, assign a default value or handle the case
                        if created is None:
                            created = timezone.now()  # Set to current time if not available
                        # If 'modified' is still None, assign it to 'created' or current time
                        if modified is None:
                            modified = created if created else timezone.now()  # Set to 'created' or current time

                        # Handle potential invalid values for numeric fields
                        try:
                            # For fields that may be missing or invalid, we check before converting to float or int
                            width = float(row["width"].replace(",", ".")) if row.get("width") else None
                            height = float(row["height"].replace(",", ".")) if row.get("height") else None
                            xres = float(row["xres"].replace(",", ".")) if row.get("xres") else None
                            yres = float(row["yres"].replace(",", ".")) if row.get("yres") else None
                            
                            # Convert to int safely
                            page_count = int(row["page_count"]) if row.get("page_count") and row["page_count"].isdigit() else None
                            
                            # If page_count is missing or invalid, set it to None or a default value
                            if not row.get("page_count") or not row["page_count"].isdigit():
                                page_count = None  # Or 0, depending on your preference
                        except ValueError as e:
                            print(f"Error converting values: {e}")
                            width = height = xres = yres = page_count = None  # Set to None if there's an error

                        # **Check for missing 'name' field**
                        name = row.get("name", "").strip() if row.get("name") else "Unnamed"  # Default to 'Unnamed' if missing
                        extension = row.get("extension", "").strip() if row.get("extension") else "unknown"

                        if not name:  # If 'name' is empty, set it to a default or skip the row
                            print("Missing 'name' in row, skipping...")
                            continue  # Skip this row or you could set a default name

                        # Save to the database
                        FileMetadata.objects.create(
                            name=name,  # Use the validated 'name'
                            extension=extension,
                            size=int(row["size"]) if row.get("size") and row["size"].isdigit() else 0,  # Default to 0 if size is invalid
                            created=created,
                            modified=modified,
                            width=width,
                            height=height,
                            xres=xres,
                            yres=yres,
                            page_count=page_count,
                        )

            except Exception as e:
                print(f"Error during CSV processing: {e}")
                return render(request, "spacexapp/upload_error.html", {"error": str(e)})

            return render(request, "spacexapp/upload_success.html")
    else:
        form = CSVUploadForm()

    return render(request, "spacexapp/upload_csv.html", {"form": form})

def upload_success(request):
    return render(request, 'spacexapp/upload_success.html')

def analyze_files(request):
    # статистика файлов по расширениям
    stats_by_extension = (
        FileMetadata.objects
        .values('extension')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # топ 10 самых больших файлов
    largest_files = FileMetadata.objects.order_by('-size')[:10]

    # топ 10 изображений по площади (ширина * высота)
    largest_images = (
        FileMetadata.objects
        .filter(extension__in=['.jpg', '.png', '.jpeg', '.bmp', '.gif'])  # Только изображения
        .exclude(Q(width__isnull=True) | Q(height__isnull=True) | Q(width=0) | Q(height=0))  # Исключаем записи с пустыми или нулевыми значениями
        .annotate(area=F('width') * F('height'))  # Рассчитываем площадь
        .order_by('-area')[:10]  # Сортируем по убыванию площади
    )

    # топ 10 документов по количеству страниц
    largest_docs = (
        FileMetadata.objects
        .filter(extension__in=['.pdf', '.doc', '.docx', '.ppt', '.pptx'])
        .exclude(Q(page_count__isnull=True) | Q(page_count=0))  # Исключаем записи с отсутствующим числом страниц
        .order_by('-page_count')[:10]
    )

    # общий размер файлов в байтах
    total_size = FileMetadata.objects.aggregate(total=Sum('size'))['total'] or 0

    # размер в гигабайты
    total_size_gb = total_size / (1024 ** 3)

    context = {
        'stats_by_extension': stats_by_extension,
        'largest_files': largest_files,
        'largest_images': largest_images,
        'largest_docs': largest_docs,
        'total_size_gb': total_size_gb,
    }



    return render(request, "spacexapp/analyze_files.html", context)


