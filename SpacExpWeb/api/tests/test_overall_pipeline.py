from django.test import TestCase, Client
from django.urls import reverse
from api.models import FileRecord
import tempfile
import os
from datetime import datetime

class FileProcessingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_file_upload_and_processing(self):
        # временный файл
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Temporary file content")
            temp_file_name = temp_file.name

        with open(temp_file_name, "rb") as file:
            response = self.client.post(
                reverse("process_files"),
                {"files": [file]},
                format="multipart",
            )

        self.assertEqual(response.status_code, 302)  # Редирект на статистику
        self.assertTrue(FileRecord.objects.exists())  # Записи в базе

        # Удаление временного файла
        os.unlink(temp_file_name)

    def test_invalid_folder_path(self):
        response = self.client.post(
            reverse("process_files"), {"folder_path": "/nonexistent/path/"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/error_page.html")
        self.assertIn("Несуществующий путь к папке.", response.content.decode())

    def test_statistics_by_extension(self):
        # тестовые записи
        FileRecord.objects.create(file_name="file1.doc", file_size=1024, extension=".doc", creation_time=datetime.now(), modification_time=datetime.now())
        FileRecord.objects.create(file_name="file2.jpg", file_size=2048, extension=".jpg", creation_time=datetime.now(), modification_time=datetime.now())
        FileRecord.objects.create(file_name="file3.txt", file_size=512, extension=".txt", creation_time=datetime.now(), modification_time=datetime.now())

        response = self.client.get(reverse("statistics_api"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("file_statistics", data)
        self.assertEqual(data["file_statistics"][0]["extension"], ".txt")
        self.assertEqual(data["file_statistics"][0]["count"], 1)

    def test_index_page_content(self):
        FileRecord.objects.create(file_name="file1.mp3", file_size=1024, extension=".mp3", creation_time=datetime.now(), modification_time=datetime.now())

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Общий объём проиндексированных файлов: <strong>1.00 KB</strong>")
        self.assertContains(response, "Количество файлов: <strong>1</strong>")

    def test_largest_image_calculation(self):
        # записи изображений с размерами
        FileRecord.objects.create(file_name="image1.jpg", file_size=1024, width=200, height=300, type="image", creation_time=datetime.now(), modification_time=datetime.now())
        FileRecord.objects.create(file_name="image2.jpg", file_size=2048, width=500, height=400, type="image", creation_time=datetime.now(), modification_time=datetime.now())

        response = self.client.get(reverse("statistics_api"))
        self.assertEqual(response.status_code, 200)
        data = response.json()

        largest_images = data["largest_images"]
        self.assertEqual(len(largest_images), 2)
        self.assertEqual(largest_images[0]["file_name"], "image2.jpg")
        self.assertEqual(largest_images[0]["calculated_area"], 500 * 400)
