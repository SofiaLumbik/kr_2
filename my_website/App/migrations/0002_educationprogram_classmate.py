# Generated by Django 5.2.1 on 2025-05-28 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_name', models.CharField(max_length=100)),
                ('my_surname', models.CharField(max_length=100)),
                ('my_phone', models.CharField(max_length=20)),
                ('my_photo', models.ImageField(upload_to='program/')),
                ('supervisor_name', models.CharField(max_length=100)),
                ('supervisor_surname', models.CharField(blank=True, max_length=100, null=True)),
                ('supervisor_email', models.EmailField(max_length=254)),
                ('supervisor_photo', models.ImageField(upload_to='program/')),
                ('manager_name', models.CharField(max_length=100)),
                ('manager_surname', models.CharField(blank=True, max_length=100, null=True)),
                ('manager_email', models.EmailField(max_length=254)),
                ('manager_photo', models.ImageField(upload_to='program/')),
                ('program_name', models.CharField(max_length=100)),
                ('program_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Classmate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='program/')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classmates', to='App.educationprogram')),
            ],
        ),
    ]
