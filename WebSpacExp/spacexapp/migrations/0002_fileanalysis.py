# Generated by Django 5.1.4 on 2024-12-16 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spacexapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=500)),
                ('file_name', models.CharField(max_length=255)),
                ('file_size', models.BigIntegerField()),
                ('creation_time', models.DateTimeField()),
                ('modification_time', models.DateTimeField()),
                ('extension', models.CharField(max_length=50)),
            ],
        ),
    ]
