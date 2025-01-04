from django.test import TestCase
from api.models import FileRecord
from datetime import datetime
import random
import string
from django.db.models import Sum, Avg, Max

class MassInsertTest(TestCase):
    """
    Тест массовой вставки данных.
    Этот тест проверяет, как база данных справляется с массовой вставкой данных.
    """
    def test_mass_insert(self):
        num_records = 10000  # количество записей для вставки
        file_records = [
            FileRecord(
                file_path=f"/path/to/file_{i}.docx",
                file_name=f"file_{i}.docx",
                file_size=random.randint(1024, 1024 * 1024 * 10),
                creation_time=datetime.now(),
                modification_time=datetime.now(),
                extension=".docx",
                type="document",
                page_count=random.randint(1, 100),
                width=None,
                height=None,
                area=None,
                sheet_names=None,
            )
            for i in range(num_records)
        ]
        FileRecord.objects.bulk_create(file_records)  # `bulk_create` для вставки
        self.assertEqual(FileRecord.objects.count(), num_records)

class MassReadTest(TestCase):
    """
    Тест массового чтения данных
    Этот тест оценивает производительность массового чтения данных из базы.
    """
    @classmethod
    def setUpTestData(cls):
        num_records = 10000
        file_records = [
            FileRecord(
                file_path=f"/path/to/file_{i}.docx",
                file_name=f"file_{i}.docx",
                file_size=random.randint(1024, 1024 * 1024 * 10),
                creation_time=datetime.now(),
                modification_time=datetime.now(),
                extension=".docx",
                type="document",
                page_count=random.randint(1, 100),
            )
            for i in range(num_records)
        ]
        FileRecord.objects.bulk_create(file_records)

    def test_mass_read(self):
        file_records = FileRecord.objects.all()
        self.assertEqual(file_records.count(), 10000)


class AggregateQueryTest(TestCase):
    """
    Тест сложных агрегатных запросов
    Этот тест проверяет, как база справляется с вычислением сложных агрегатных запросов.
    """
    @classmethod
    def setUpTestData(cls):
        for i in range(10000):
            FileRecord.objects.create(
                file_path=f"/path/to/file_{i}.docx",
                file_name=f"file_{i}.docx",
                file_size=random.randint(1024, 1024 * 1024 * 10),
                creation_time=datetime.now(),
                modification_time=datetime.now(),
                extension=".docx",
                type="document",
                page_count=random.randint(1, 100),
            )

    def test_aggregate_query(self):
        total_size = FileRecord.objects.aggregate(Sum("file_size"))["file_size__sum"]
        avg_page_count = FileRecord.objects.aggregate(Avg("page_count"))["page_count__avg"]
        largest_file = FileRecord.objects.aggregate(Max("file_size"))["file_size__max"]

        self.assertIsNotNone(total_size)
        self.assertIsNotNone(avg_page_count)
        self.assertIsNotNone(largest_file)

class PaginationTest(TestCase):
    """
    Тест пагинации результатов
    Этот тест проверяет производительность при использовании пагинации для работы с большими наборами данных.
    """
    @classmethod
    def setUpTestData(cls):
        for i in range(10000):
            FileRecord.objects.create(
                file_path=f"/path/to/file_{i}.docx",
                file_name=f"file_{i}.docx",
                file_size=random.randint(1024, 1024 * 1024 * 10),
                creation_time=datetime.now(),
                modification_time=datetime.now(),
                extension=".docx",
                type="document",
                page_count=random.randint(1, 100),
            )

    def test_pagination(self):
        page_size = 100
        total_records = FileRecord.objects.count()
        total_pages = (total_records + page_size - 1) // page_size

        for page in range(total_pages):
            offset = page * page_size
            records = FileRecord.objects.all()[offset:offset + page_size]
            self.assertLessEqual(len(records), page_size)


class MassDeleteTest(TestCase):
    """
    Тест удаления большого количества данных
    Этот тест проверяет производительность массового удаления записей.
    """
    @classmethod
    def setUpTestData(cls):
        for i in range(10000):
            FileRecord.objects.create(
                file_path=f"/path/to/file_{i}.docx",
                file_name=f"file_{i}.docx",
                file_size=random.randint(1024, 1024 * 1024 * 10),
                creation_time=datetime.now(),
                modification_time=datetime.now(),
                extension=".docx",
                type="document",
                page_count=random.randint(1, 100),
            )

    def test_mass_delete(self):
        FileRecord.objects.all().delete()
        self.assertEqual(FileRecord.objects.count(), 0)
