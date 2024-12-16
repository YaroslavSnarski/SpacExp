from django.db import models

class FileAnalysis(models.Model):
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # Размер файла в байтах
    creation_time = models.DateTimeField()
    modification_time = models.DateTimeField()
    extension = models.CharField(max_length=50)
    image_width = models.IntegerField(null=True, blank=True)  # Только для изображений
    image_height = models.IntegerField(null=True, blank=True)  # Только для изображений
    num_pages = models.IntegerField(null=True, blank=True)  # Только для документов
    
    def __str__(self):
        return self.file_name
