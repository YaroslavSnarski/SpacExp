from django.test import TestCase, Client
from django.urls import reverse
from api.models import FileRecord
from datetime import datetime
import tempfile
import os
import json
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class FileManagerTests(TestCase):
    def test_process_files_in_temp_directory(self):
        """Тест обработки временной папки с файлами."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем тестовые файлы
            for i in range(3):
                file_path = os.path.join(temp_dir, f"test_file{i}.txt")
                with open(file_path, "w") as file:
                    file.write("Sample content")

            # проверяем, что FileManager корректно обрабатывает файлы
            from SpacExp.file_manager import FileManagerWeb
            file_manager = FileManagerWeb(temp_dir)
            results = file_manager.process_files()
            self.assertEqual(len(results), 3)
            for result in results:
                self.assertIn("file_name", result)
                self.assertIn("file_size", result)

    def test_process_files_no_files(self):
        """Тест обработки пустой папки."""
        with tempfile.TemporaryDirectory() as temp_dir:
            from SpacExp.file_manager import FileManagerWeb
            file_manager = FileManagerWeb(temp_dir)
            results = file_manager.process_files()
            self.assertEqual(len(results), 0)


class ErrorHandlingTests(TestCase):
    def test_invalid_request_method(self):
        """Тест обработки некорректного HTTP метода."""
        response = self.client.get(reverse('process_files'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверный метод запроса.")