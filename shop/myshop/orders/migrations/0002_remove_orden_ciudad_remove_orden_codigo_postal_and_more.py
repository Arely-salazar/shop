# Generated by Django 5.0.3 on 2024-05-12 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='codigo_postal',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='direccion',
        ),
    ]