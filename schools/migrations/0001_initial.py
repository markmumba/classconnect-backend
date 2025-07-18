# Generated by Django 5.2.3 on 2025-06-26 07:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('email_domain', models.CharField(max_length=100, unique=True)),
                ('location', models.TextField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='school_logo/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'school',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SubSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='schools.school')),
            ],
            options={
                'db_table': 'sub_schools',
                'ordering': ['school', 'name'],
                'unique_together': {('school', 'name')},
            },
        ),
    ]
