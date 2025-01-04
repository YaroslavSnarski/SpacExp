from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import FileRecord
from django.test import TestCase
import os

class StatisticsTests(TestCase):
    def test_statistics_page(self):
        """
        Testing that a statistics pages renders.
        """
        FileRecord.objects.create(
            file_name="test_image.gif", file_size=100, extension=".gif", type="image",
            creation_time="2024-01-01", modification_time="2024-01-01"
        )
        response = self.client.get(reverse('statistics_page'))
        
        # успешный рендер страницы
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Топ самых больших файлов")
        self.assertContains(response, "test_image.gif")

    def test_statistics_api_view(self):
        """
        Testing API to collect statistics
        """
        FileRecord.objects.create(
            file_name="test_image.gif", file_size=100, extension=".gif", type="image",
            creation_time="2024-01-01", modification_time="2024-01-01"
        )
        
        response = self.client.get(reverse('statistics_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # статистика
        self.assertIn("file_statistics", data)
        self.assertIn("largest_files", data)
        self.assertIn("largest_images", data)
        self.assertIn("largest_documents", data)

    def test_empty_statistics(self):
        """
        Testing when no data requested
        """
        response = self.client.get(reverse('statistics_api'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        self.assertEqual(data['file_statistics'], [])
        self.assertEqual(data['largest_files'], [])
        self.assertEqual(data['largest_images'], [])
        self.assertEqual(data['largest_documents'], [])
