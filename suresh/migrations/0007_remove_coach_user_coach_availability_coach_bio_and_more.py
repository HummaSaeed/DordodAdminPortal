# Generated by Django 5.0.6 on 2025-05-23 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0006_coachrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='user',
        ),
        migrations.AddField(
            model_name='coach',
            name='availability',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='certifications',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='email',
            field=models.EmailField(default='defaul@example.com', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='languages_spoken',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='coach',
            name='social_media',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coach',
            name='specializations',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='expertise',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='coach',
            name='profile_picture',
            field=models.URLField(blank=True, null=True),
        ),
    ]
