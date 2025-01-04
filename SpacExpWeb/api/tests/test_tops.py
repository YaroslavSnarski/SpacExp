from django.test import TestCase
from api.models import FileRecord
from django.urls import reverse

class StatisticsAPITests1(TestCase):
    
    def setUp(self):
        # создаем тестовые файлы с разными размерами
        FileRecord.objects.create(
            file_name="small_file.doc",
            file_size=1000,
            type="document",
            extension=".doc",
            creation_time="2024-12-01",
            modification_time="2024-12-01",
        )
        FileRecord.objects.create(
            file_name="large_file.doc",
            file_size=5000000,  # 5MB
            type="document",
            extension=".doc",
            creation_time="2024-12-01",
            modification_time="2024-12-01",
        )

    def test_largest_files_in_statistics1(self):
        # посылаем GET-запрос на statistics API
        response = self.client.get(reverse('statistics_api'))
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # largest_files содержит файл с максимальным размером
        largest_files = data['largest_files']
        self.assertGreater(largest_files[0]['file_size'], largest_files[1]['file_size'])
        self.assertEqual(largest_files[0]['file_name'], "large_file.doc")

class StatisticsAPITests2(TestCase):
    def setUp(self):
        # создаем два изображения с разными размерами
        FileRecord.objects.create(
            file_name="small_image.jpg",
            file_size=5000,
            type="image",
            extension=".jpg",
            width=100,
            height=200,
            creation_time="2024-12-01",
            modification_time="2024-12-01",
        )
        FileRecord.objects.create(
            file_name="large_image.jpg",
            file_size=15000,
            type="image",
            extension=".jpg",
            width=500,
            height=400,
            creation_time="2024-12-01",
            modification_time="2024-12-01",
        )

    def test_largest_images_in_statistics2(self):
        # посылаем GET-запрос на statistics API
        response = self.client.get(reverse('statistics_api'))
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # largest_images содержит файл с максимальной площадью
        largest_images = data['largest_images']
        self.assertGreater(largest_images[0]['calculated_area'], largest_images[1]['calculated_area'])
        self.assertEqual(largest_images[0]['file_name'], "large_image.jpg")

class StatisticsAPITests3(TestCase):
    def setUp(self):
        # cоздаем два документа с разным количеством страниц
        FileRecord.objects.create(
            file_name="small_document.docx",
            file_size=3000,
            type="document",
            extension=".docx",
            page_count=5,
            creation_time="2024-12-01",
            modification_time="2024-12-01",
        )
        FileRecord.objects.create(
            file_name="large_document.docx",
            file_size=20000,
            type="document",
            extension=".docx",
            page_count=50,
            creation_time="2024-12-01",
            modification_time="2024-12-01",
        )

    def test_largest_documents_in_statistics3(self):
        # посылаем GET-запрос на statistics API
        response = self.client.get(reverse('statistics_api'))
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # largest_documents содержит файл с наибольшим количеством страниц
        largest_documents = data['largest_documents']
        self.assertGreater(largest_documents[0]['page_count'], largest_documents[1]['page_count'])
        self.assertEqual(largest_documents[0]['file_name'], "large_document.docx")
