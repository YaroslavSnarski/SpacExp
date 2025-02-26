# Generated by Django 5.1.4 on 2024-12-20 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_imagefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=500)),
                ('file_name', models.CharField(max_length=200)),
                ('file_size', models.BigIntegerField()),
                ('creation_time', models.DateTimeField()),
                ('modification_time', models.DateTimeField()),
                ('extension', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=50)),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('area', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
