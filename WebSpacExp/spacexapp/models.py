from django.db import models

class FileRecord(models.Model):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class FileAnalysis(models.Model):
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    creation_time = models.DateTimeField()
    modification_time = models.DateTimeField()
    extension = models.CharField(max_length=50)
    
    def __str__(self):
        return self.file_name


class FileMetadata(models.Model):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=50)
    size = models.IntegerField()  # Размер в байтах
    width = models.IntegerField(null=True, blank=True)  
    height = models.IntegerField(null=True, blank=True)  
    created = models.DateTimeField()
    modified = models.DateTimeField()
    xres = models.IntegerField(null=True, blank=True)  # xres field
    yres = models.IntegerField(null=True, blank=True)  # yres field
    page_count = models.IntegerField(null=True, blank=True)  # page_count field


    def __str__(self):
        return self.name