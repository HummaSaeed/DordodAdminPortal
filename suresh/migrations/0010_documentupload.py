# Generated by Django 5.0.6 on 2024-09-22 10:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suresh', '0009_alter_professionalinformation_honors_awards_publications_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('resume', 'Resume'), ('cover_letter', 'Cover Letter'), ('portfolio', 'Portfolio'), ('education', 'Educational Document'), ('professional', 'Professional Document'), ('bank', 'Bank Document'), ('other', 'Other Document')], max_length=20)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
