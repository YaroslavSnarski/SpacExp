# Generated by Django 5.1.4 on 2024-12-16 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spacexapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileanalysis',
            old_name='height',
            new_name='image_height',
        ),
        migrations.RenameField(
            model_name='fileanalysis',
            old_name='page_count',
            new_name='image_width',
        ),
        migrations.RenameField(
            model_name='fileanalysis',
            old_name='width',
            new_name='num_pages',
        ),
    ]
