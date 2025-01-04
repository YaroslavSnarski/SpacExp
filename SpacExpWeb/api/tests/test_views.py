from django.test import TestCase, Client
from django.urls import reverse
from api.models import FileRecord
from datetime import datetime

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client() # тестовый клиент Django, который имитирует HTTP-запросы
        # тут создадим тестовые записи для doc и jpg файлов
        FileRecord.objects.create(
            file_path="/path/to/file",
            file_name="file1.doc",
            file_size=1024,
            creation_time=datetime.now(),
            modification_time=datetime.now(),
            extension=".doc",
            type="document",
        )
        FileRecord.objects.create(
            file_path="/path/to/image",
            file_name="image1.jpg",
            file_size=2048,
            creation_time=datetime.now(),
            modification_time=datetime.now(),
            extension=".jpg",
            type="image",
            width=1920,
            height=1080,
        )

    def test_index_view(self): # главная страница (index) загружается успешно и отображает текст
        """Test the index view returns the correct context data"""
        response = self.client.get(reverse('index')) # отправляем GET-запрос к URL, связанному с именем маршрута index.
        self.assertEqual(response.status_code, 200) # чек кода ответа - отправлили ли запрос успешно?
        self.assertContains(response, "Общий объём проиндексированных файлов") # вернувшийся ответ содержит текстовую часть хтмл-кода

    def test_statistics_view(self): # страница статистики (statistics_page) рендерится и отображает текст
        """Test the statistics view renders correctly"""
        response = self.client.get(reverse('statistics_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Статистика по файлам")

    def test_process_files_view_no_data(self): # представление корректно обрабатывает случай, когда данные не переданы
        """Test POST request to process_files_view with no data"""
        response = self.client.post(reverse('process_files'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Вы не выбрали папку. Пожалуйста, выберите папку")

    def test_process_files_view_with_folder(self): # представление корректно обрабатывает некорректный путь к папке
        """Test POST request to process_files_view with a folder path"""
        response = self.client.post(reverse('process_files'), {"folder_path": "/invalid/path"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Несуществующий путь к папке")

    def test_statistics_api_view(self): # API возвращает корректные данные в JSON-формате
        """Test the statistics API endpoint"""
        response = self.client.get(reverse('statistics_api'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("file_statistics", response.json())

    def test_largest_files_statistics(self): # статистика о самых больших файлах рассчитывается корректно?
        """Test that largest files are correctly calculated in statistics"""
        response = self.client.get(reverse('statistics_api'))
        largest_files = response.json().get("largest_files", [])
        self.assertEqual(len(largest_files), 2)
        self.assertEqual(largest_files[0]["file_name"], "image1.jpg")
