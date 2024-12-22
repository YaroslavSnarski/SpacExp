from django.db import models

class FileRecord(models.Model):
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=200)
    file_size = models.BigIntegerField()  # Размер файла
    creation_time = models.DateTimeField()
    modification_time = models.DateTimeField()
    extension = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    page_count = models.IntegerField(null=True, blank=True)  # Только для документов
    width = models.IntegerField(null=True, blank=True)  # Только для изображений
    height = models.IntegerField(null=True, blank=True)  # Только для изображений
    area = models.IntegerField(null=True, blank=True)  # Ширина x Высота (для изображений)
    sheet_names = models.JSONField(default=list, blank=True, null=True)  # JSONField для хранения списка и разрешаем пустое значение

    def __str__(self):
        return self.file_name
