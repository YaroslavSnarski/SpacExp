from django.test import TestCase
from api.models import FileRecord
from datetime import datetime

class FileRecordModelTest(TestCase):
    def setUp(self):
        self.file_record = FileRecord.objects.create(
            file_path="/path/to/file",
            file_name="test_file.docx",
            file_size=1024,
            creation_time=datetime.now(),
            modification_time=datetime.now(),
            extension=".docx",
            type="document",
            page_count=10,
            width=None,
            height=None,
            area=None,
            sheet_names=None,
        )

    def test_file_record_creation(self): # чек, что объект модели корректно сохраняется в базу данных с переданными параметрами
        """Test that a FileRecord instance is created correctly"""
        self.assertEqual(FileRecord.objects.count(), 1) # число записей в модели FileRecord равно 1 после создания объекта
        self.assertEqual(self.file_record.file_name, "test_file.docx") # название файла (file_name) для объекта соответствует значению, которое передавалось при создании.


    def test_default_values(self): # чек, что для необязательных полей (width, height) используются значения None по умолчанию
        """Test default values for optional fields""" 
        self.assertIsNone(self.file_record.width) # нужно быть уверенными, что необязательные поля имеют правильные значения по умолчанию, если они не заданы. 
        self.assertIsNone(self.file_record.height) # иначе могут быть ошибки, связанные с неправильной инициализацией данных.

    def test_update_file_record(self): # чек возможности обновления объекта FileRecord - убаждаемся, что данные объекта модели обновляются, изменения сохраняются корректно в базе данных.
        """Test updating an existing record"""
        self.file_record.file_name = "updated_file.docx" # заменяет значение поля file_name на "updated_file.docx".
        self.file_record.save() # сохраняет изменения в базе данных
        updated_record = FileRecord.objects.get(id=self.file_record.id)
        self.assertEqual(updated_record.file_name, "updated_file.docx") # извлекает объект из базы данных и проверяет, что обновленное значение соответствует ожидаемому.

    def test_deletion(self): # возможность удаления объекта FileRecord
        """Test deleting a record"""
        self.file_record.delete()
        self.assertEqual(FileRecord.objects.count(), 0) # чек, что общее количество записей в модели равно 0.

