# Generated by Django 2.2.4 on 2021-08-06 11:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fqa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('contact_number', models.CharField(max_length=15, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('contact_number', models.CharField(max_length=15, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='John Doe', max_length=32)),
                ('kind', models.CharField(choices=[('DOG', 'Dog'), ('CAT', 'Cat'), ('BIRD', 'Bird'), ('FISH', 'Fish'), ('OTHER', 'Other')], default='DOG', max_length=10)),
                ('description', models.CharField(blank=True, max_length=256)),
                ('picture', models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')),
                ('date_of_arrival', models.DateField(blank=True, default=datetime.date.today)),
                ('adoption_status', models.CharField(choices=[('ADOPTED', 'Adopted'), ('NOT_ADOPTED', 'Waiting for a home'), ('REQUESTED', 'Request pending'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=16)),
                ('adoption_date', models.DateField(blank=True, null=True)),
                ('shelter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bolt.Shelter')),
            ],
        ),
    ]
