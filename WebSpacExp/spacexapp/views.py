import csv
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .forms import CSVUploadForm
from .models import FileMetadata
from django.db.models import Count, F, Q, Sum
from django.db import transaction

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
