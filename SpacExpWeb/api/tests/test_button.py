from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

class FormButtonTest(TestCase):
    def test_analyze_button_redirects_to_results(self):
        # файл для загрузки
        file = SimpleUploadedFile('test.txt', b'File content', content_type='text/plain')
        
        # отправим формы через POST-запрос
        response = self.client.post(reverse('process_files'), {'files': [file]})
        
        # чек, что происходит редирект после отправки формы 
        self.assertEqual(response.status_code, 302)  # Проверка редиректа
        self.assertRedirects(response, reverse('statistics_page'))
        
    def test_analyze_button_with_multiple_files(self):
        # то же самое, но с 1000 файлов
        files = []
        for i in range(1, 1001):
            file = SimpleUploadedFile(f'file{i}.txt', f'Content of file {i}'.encode(), content_type='text/plain')
            files.append(file)
        
        # отправляем формы с 1000 файлами
        response = self.client.post(reverse('process_files'), {'files': files})
        
        # чек, что редирект после отправки формы 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statistics_page'))
        