# Generated by Django 5.1.4 on 2024-12-10 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('extension', models.CharField(max_length=50)),
                ('size', models.IntegerField()),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('xres', models.IntegerField(blank=True, null=True)),
                ('yres', models.IntegerField(blank=True, null=True)),
                ('page_count', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
