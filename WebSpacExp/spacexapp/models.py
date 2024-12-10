from django.db import models


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