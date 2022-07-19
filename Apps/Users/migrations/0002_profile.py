# Generated by Django 4.0 on 2022-04-17 21:00

import Storage.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(error_messages={'unique': 'This nickname already exists.'}, max_length=50, null=True, unique=True, verbose_name='Nick')),
                ('bio', models.TextField(null=True, verbose_name='Bio')),
                ('image', models.ImageField(null=True, upload_to=Storage.storage.image_file_upload, verbose_name='Profile image')),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('N', 'Non-binary'), ('P', 'Prefer not to say')], default='P', max_length=1, null=True, verbose_name='Gender')),
                ('preferred_language', models.CharField(choices=[('EN', 'English'), ('ES', 'Spanish'), ('FR', 'French'), ('OT', 'Other')], default='OT', max_length=2, null=True, verbose_name='Preferred language')),
                ('birth_date', models.DateField(null=True, verbose_name='Birth date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='Users.user')),
            ],
        ),
    ]
