# Generated by Django 5.0.6 on 2025-06-16 20:33

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0007_remove_coach_user_coach_availability_coach_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name='MoodTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_mood', models.CharField(choices=[('Happy', 'Happy'), ('Excited', 'Excited'), ('Calm', 'Calm'), ('Focused', 'Focused'), ('Tired', 'Tired'), ('Stressed', 'Stressed'), ('Anxious', 'Anxious'), ('Frustrated', 'Frustrated')], max_length=20)),
                ('energy_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('stress_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('notes', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
